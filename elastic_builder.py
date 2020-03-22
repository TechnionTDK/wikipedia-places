import urllib.parse

import requests
import json

from idna import unicode

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

        # print("size:")
        # print("self.allLabels: ", self.allLabels.__len__())
        # print("self.labelsToUrls: ", self.labelsToUrls.__len__())
        # print("self.urlsToAbstract: ", self.urlsToAbstract.__len__())

        testLabel = "מתמטיקה"
        url = self.labelsToUrls[testLabel]
        print(testLabel, url)
        print(self.urlsToAbstract[url])


    def __labelsAndUrlsFromJson(self):
        with open(r"input/wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
            labelsAndUrls = json.load(read_file)
        # saves in better data structures
        for labelDict in labelsAndUrls:
            label = labelDict['rdfs:label']
            self.allLabels.append(label)
            self.labelsToUrls[label] = labelDict['uri']





            # self.labelsToUrls[label] = urllib.parse.quote(labelDict['uri'])
            # self.labelsToUrls[label] = labelDict['uri'].strip().encode('utf-8')
            # url = unicode(labelDict['uri'])#.strip().encode('idna')
            # # url2 = labelDict['uri'].strip().encode('idna')
            # url3 = labelDict['uri'].strip().encode('utf-8')
            # url4 = labelDict['uri'].encode('idna')






    def __abstractsFromJson(self):
        with open(r"input/wiki_hebrew_abstracts.json", "r", encoding='utf-8') as read_file:
            abstractsAndUrls = json.load(read_file)
        # saves in better data structures
        for abstractDict in abstractsAndUrls:

            url = urllib.parse.unquote(abstractDict['uri'])
            self.urlsToAbstract[url] = abstractDict['dbo:abstract']




            # url2 = abstractDict['uri'].strip().encode('idna')
            #             # url3 = abstractDict['uri'].strip().encode('utf-8')
            #             # url4 = abstractDict['uri'].encode('idna')
            #             # print(url)


# allLabels = ["הקרב על גבעת התחמושת", "בית הספר לשוטרים (ירושלים)", "בית הספר רנה קסין", "קריית הממשלה (מזרח ירושלים)", "שכונות הבריח", "קריית הלאום", "יד הזיכרון למגיני ירושלים",
#           "הרי יהודה", "סנהדריה המורחבת", "ישיבת תפארת צבי", "ישיבת מיר", "נחל צופים", "נבי סמואל", "שדרות בר-לב",
#           "גן העצמאות (ירושלים)", "דרך שכם", "קבר רחל", "תחנת הרכבת ההיסטורית של ירושלים", "פארק אירופה", "דיסנילנד פריז"]




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
        # R = S.get(url=URL, params=PARAMS)
        # DATA = R.json()
        # PAGES = DATA['query']['pages']
        # for k, v in PAGES.items():
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
        # with open('output/' + doc["label"] + '.json', 'w', encoding='utf-8') as outfile:
        #     json.dump(doc, outfile, ensure_ascii=False)
        res = S.post(url='http://localhost:9200/nerya/_doc/'+doc["label"], headers={'Content-Type': 'application/json'}, json=doc)
        print("start indexing label " + doc["label"] + "...")

# for label in allLabels:p
#     # es.index(index="nerya", doc_type='_doc', id=label,body=doc)
#     print("start indexing lable "+label+ "...")
#     res = S.post(url='http://localhost:9200/nerya/_doc/'+label, headers={'Content-Type': 'application/json'}, json=elas_doc)
#     print("finished indexing lable "+label+"!")



# for label in labels:
#     if label not in results:
#         print(label)


def main():
    data = dataLoad()
    elasticDocs = saveWithCoordinates(data)
    elasticBuilder(elasticDocs)

if __name__ == "__main__":
    main()