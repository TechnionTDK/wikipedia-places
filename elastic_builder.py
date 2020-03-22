import requests
import json
import urllib.parse

S = requests.Session()


class dataLoad:
    def __init__(self):
        # data structures
        self.allLabels = []
        self.labelsToUrls = {}
        self.urlsToAbstract = {}

        # get data
        self.__labelsAndUrlsFromJson()
        self.__abstractsFromJson()


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
            url = urllib.parse.unquote(abstractDict['uri'])
            self.urlsToAbstract[url] = abstractDict['dbo:abstract']



def saveWithCoordinates(data):
    #init
    URL = "https://he.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "",
        "prop": "coordinates"
    }
    docs = []

    #saves
    for label in data.allLabels:
        PARAMS["titles"] = label
        for k, v in S.get(url=URL, params=PARAMS).json()['query']['pages'].items():
            if 'coordinates' in v:
                fullCoordinates = v['coordinates'][0]
                coordinates = {
                    "lat": fullCoordinates['lat'],
                    "lon": fullCoordinates['lon']
                }
                url = data.labelsToUrls[label]
                abstract = ""
                if url in data.urlsToAbstract:
                    abstract = data.urlsToAbstract[url]
                doc = {
                    "label": label,
                    "coordinates": coordinates,
                    "url": url,
                    "abstract": abstract
                }
                print(doc)
                with open('output/' + doc["label"] + '.json', 'w', encoding='utf-8') as outfile:
                    json.dump(doc, outfile, ensure_ascii=False)
                docs.append(doc)
    return docs


def elasticBuilder(elasticDocs):
    for doc in elasticDocs:
        print("start indexing label " + doc["label"] + "...")
        res = S.post(url='http://localhost:9200/nerya/_doc/'+doc["label"], headers={'Content-Type': 'application/json'}, json=doc)
        print("start indexing label " + doc["label"] + "...")


def main():
    data = dataLoad()
    elasticDocs = saveWithCoordinates(data)
    elasticBuilder(elasticDocs)

if __name__ == "__main__":
    main()