import re
import requests
import json

from elasticsearch import Elasticsearch

S = requests.Session()
index = "all"


def connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def restartElasticIndex():
    es = connect()
    for i in es.indices.get('*'):
        if i == index:
            es.indices.delete(index=i)


def toFilename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def coordinatesOnEarth(fullCoordinates):
    return abs(fullCoordinates['lat']) <= 90 and abs(fullCoordinates['lon']) <= 180


class dataLoad:
    def __init__(self):
        # data structures
        self.allLabels = []
        self.labelsToUrls = {}
        self.urlsToAbstract = {}

        # get data
        self.__labelsAndUrlsFromJson()
        self.__abstractsFromJson()

        print(self.allLabels.__len__())
        print("labels size: ", self.labelsToUrls.__len__())
        print("abstacts size: ", self.urlsToAbstract.__len__())
        print("finish dataLoad")

    def __labelsAndUrlsFromJson(self):
        with open(r"input/wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
            labelsAndUrls = json.load(read_file)
        # saves in better data structures
        for labelDict in labelsAndUrls:
            label = labelDict['rdfs:label']
            self.allLabels.append(label)
            self.labelsToUrls[label] = labelDict['uri']

    def __abstractsFromJson(self):
        with open(r"input/wiki_hebrew_abstracts.json", "r", encoding='utf-8') as read_file:
            abstractsAndUrls = json.load(read_file)
        # saves in better data structures
        for abstractDict in abstractsAndUrls:
            url = abstractDict['uri']
            self.urlsToAbstract[url] = abstractDict['dbo:abstract']


def saveWithCoordinates(data):
    # init
    URL = "https://he.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "",
        "prop": "coordinates"
    }
    docs = []

    # saves
    for label in data.allLabels:
        PARAMS["titles"] = label
        for k, v in S.get(url=URL, params=PARAMS).json()['query']['pages'].items():
            if 'coordinates' in v and coordinatesOnEarth(v['coordinates'][0]):
                fullCoordinates = v['coordinates'][0]
                coordinates = {
                    "lat": fullCoordinates['lat'],
                    "lon": fullCoordinates['lon']
                }
                url = data.labelsToUrls[label]
                abstract = ""
                if url in data.urlsToAbstract:
                    abstract = data.urlsToAbstract[url]
                pin = {"location":
                           coordinates
                       }
                doc = {
                    "label": label,
                    "pin": pin,
                    "url": url,
                    "abstract": abstract
                }
                # print(doc)
                # with open('output/' + toFilename(doc["label"]) + '.json', 'w',
                #           encoding='utf-8') as outfile:  # for saving the files on your computer
                #     json.dump(doc, outfile, ensure_ascii=False)
                docs.append(doc)
    return docs


def elasticBuilder(elasticDocs):
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
        print("start indexing label " + doc["label"] + "...")
        es.index(index=index, body=doc)
        print("finish indexing label " + doc["label"] + "...")


def main():
    data = dataLoad()
    elasticDocs = saveWithCoordinates(data)
    restartElasticIndex()
    elasticBuilder(elasticDocs)


if __name__ == "__main__":
    main()
