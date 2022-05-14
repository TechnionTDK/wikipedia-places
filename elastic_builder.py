import re
import requests
import json
from datetime import datetime
from elasticsearch import Elasticsearch

file = None
S = requests.Session()
index = "all"
allowedImageSuffix = ".jpg"
defaultMinAbstractSentences = 5
URL = "https://he.wikipedia.org/w/api.php"


def reportProcess(report):
    global file
    today = datetime.today()
    report = f'{today.strftime("%d/%m/%Y %H:%M:%S")}: {str(report)}\n'
    file.write(report)
    print(report)


def connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def restartElasticIndex():
    reportProcess("restartElasticIndex started")
    es = connect()
    for i in es.indices.get('*'):
        if i == index:
            es.indices.delete(index=i)
    reportProcess("restartElasticIndex finished")


def toFilename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def coordinatesOnEarth(fullCoordinates):
    return abs(fullCoordinates['lat']) <= 90 and abs(fullCoordinates['lon']) <= 180


def filterAbstract(abstract):
    abstract = re.sub(r'[0-9]+[p][x]', "", abstract)
    abstract = re.sub(r'(<[a-z]*>)', "", abstract)
    abstract = abstract.replace("_", " ").replace("{", "").replace("}", "").replace("=", " ").replace("|", "").replace("==", "").replace("\n\n", "").replace("  ", " ")

    abstract = abstract.split('ראו גם')[0]
    abstract = abstract.split('לקריאה נוספת')[0]
    abstract = abstract.split('קישורים חיצוניים')[0]
    abstract = abstract.split('הערות שוליים')[0]

    if len(abstract) and abstract[0] == " ":
        abstract = abstract[1:]

    if len(abstract) and abstract[-1] == " ":
        abstract = abstract[0: -1]

    abstract_sentences = abstract.split(".")
    return " ".join(abstract_sentences[0:min(defaultMinAbstractSentences + 1, len(abstract_sentences))])


def getImageUrl(images):
    for image in images:
        if 'title' in image and allowedImageSuffix in image['title']:
            PARAMS = {
                "action": "query",
                "titles": image['title'].replace("קובץ", 'File').replace(" ", "_"),
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json"
            }
            imageInfo = S.get(url=URL, params=PARAMS).json()['query']['pages']
            if '-1' in imageInfo and 'imageinfo' in imageInfo['-1'] and len(imageInfo['-1']['imageinfo']) and 'url' in imageInfo['-1']['imageinfo'][0]:
                return imageInfo['-1']['imageinfo'][0]['url']
    return ""


class dataLoad:
    def __init__(self):
        reportProcess("start dataLoad")
        # data structures
        self.allLabels = []
        self.labelsToUrls = {}

        # get data
        self.__labelsAndUrlsFromJson()

        reportProcess(self.allLabels.__len__())
        reportProcess(f'labels size: {self.labelsToUrls.__len__()}')
        reportProcess("finish dataLoad")

    def __labelsAndUrlsFromJson(self):
        with open(r"input/wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
            labelsAndUrls = json.load(read_file)
        # saves in better data structures
        for labelDict in labelsAndUrls:
            label = labelDict['rdfs:label']
            self.allLabels.append(label)
            self.labelsToUrls[label] = labelDict['uri']



def saveWithCoordinates(data):
    reportProcess("saveWithCoordinates started!")
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "",
        "prop": "coordinates|images|extracts",
        "explaintext": 1
    }
    docs = []

    for label in data.allLabels:
        PARAMS["titles"] = label
        for k, v in S.get(url=URL, params=PARAMS).json()['query']['pages'].items():
            reportProcess(label)
            if 'coordinates' in v and coordinatesOnEarth(v['coordinates'][0]):
                url = data.labelsToUrls[label]

                pin = {"location": {
                    "lat": v['coordinates'][0]['lat'],
                    "lon": v['coordinates'][0]['lon']
                }}

                doc = {
                    "label": label,
                    "pin": pin,
                    "url": url,
                    "abstract": filterAbstract(v['extract']),
                    "imageUrl": getImageUrl(v['images']) if 'images' in v else ''
                }
                docs.append(doc)
                reportProcess(doc)
    reportProcess("saveWithCoordinates finished!")
    return docs


def elasticBuilder(elasticDocs):
    reportProcess("elasticBuilder started!")
    es = connect()
    mapping = {
        "mappings": {
            "properties": {
                "pin": {
                    "properties": {
                        "location": {
                            "type": "geo_point"
                        }
                    }
                }
            }
        }
    }
    es.indices.create(index=index, body=mapping)
    for doc in elasticDocs:
        reportProcess("start indexing label " + doc["label"] + "...")
        es.index(index=index, body=doc)
        reportProcess("finish indexing label " + doc["label"] + "...")
    reportProcess("elasticBuilder finished!")


def main():
    global file
    file = open("index_process.txt", "w")

    try:
        data = dataLoad()
        elasticDocs = saveWithCoordinates(data)
        restartElasticIndex()
        elasticBuilder(elasticDocs)
        reportProcess("============== finish successfully!!!! ==============")
        file.close()

    except Exception as e:
        reportProcess("finish with Exception!!!!")
        reportProcess(e)
        file.close()


if __name__ == "__main__":
    main()
