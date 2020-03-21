import requests
import json

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
            url = abstractDict['uri']
            self.urlsToAbstract[url] = abstractDict['dbo:abstract']


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
                doc = {
                    "label": label,
                    "coordinates": coordinates,
                    "url": url,
                    "abstract": data.urlsToAbstract[url]
                }
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