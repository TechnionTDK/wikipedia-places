import re
import requests
import json
import urllib.parse

S = requests.Session()


class dataSavingTest:
    def __init__(self):
        self.allLabels = []
        self.labelsToUrls = {}
        self.urlsToAbstract = {}
        # get data
        self.__labelsAndUrlsFromJson()
        self.__abstractsFromJson()

    def __labelsAndUrlsFromJson(self):
        with open(r"input\partialData_repaired_wiki_hebrew\wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
            labelsAndUrls = json.load(read_file)
        # saves in better data structures
        for labelDict in labelsAndUrls:
            label = labelDict['rdfs:label']
            self.allLabels.append(label)
            self.labelsToUrls[label] = labelDict['uri']

    def __abstractsFromJson(self):
        with open(r"input\partialData_repaired_wiki_hebrew\wiki_hebrew_abstracts.json", "r", encoding='utf-8') as read_file:
            abstractsAndUrls = json.load(read_file)
        # saves in better data structures
        for abstractDict in abstractsAndUrls:
            url = urllib.parse.unquote(abstractDict['uri'])
            self.urlsToAbstract[url] = abstractDict['dbo:abstract']

    def test(self, data):

        # init
        URL = "https://he.wikipedia.org/w/api.php"
        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": "",
            "prop": "coordinates"
        }
        docs = []
        allWereFound = 1
        for label in self.allLabels:
            if label not in data.allLabels:
                print("label"+label+"not in data")
                allWereFound = 0
            else:
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
                        with open('output/' + toFilename(label) + '.json', 'r', encoding='utf-8') as read_file:
                            savedData = json.load(read_file)
                        print(doc)
                        print(savedData)
                        print(doc == savedData)
        print("allWereFound(dataTest): ", allWereFound)




class dataTest:
    def __init__(self):
        self.allLabels = []
        self.labelsToUrls = {}
        self.urlsToAbstract = {}
        # get data
        self.__labelsAndUrlsFromJson()
        self.__abstractsFromJson()

    def __labelsAndUrlsFromJson(self):
        with open(r"input\partialData_repaired_wiki_hebrew\wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
            labelsAndUrls = json.load(read_file)
        # saves in better data structures
        for labelDict in labelsAndUrls:
            label = labelDict['rdfs:label']
            self.allLabels.append(label)
            self.labelsToUrls[label] = labelDict['uri']

    def __abstractsFromJson(self):
        with open(r"input\partialData_repaired_wiki_hebrew\wiki_hebrew_abstracts.json", "r", encoding='utf-8') as read_file:
            abstractsAndUrls = json.load(read_file)
        # saves in better data structures
        for abstractDict in abstractsAndUrls:
            url = urllib.parse.unquote(abstractDict['uri'])
            self.urlsToAbstract[url] = abstractDict['dbo:abstract']

    # this test make sure all labels in the partial-data files is in the extracted full data
    # in case of coordinated label this test make sure the saved data is the right data (=same as in the partial-data files)
    def test1(self, data):

        # init
        URL = "https://he.wikipedia.org/w/api.php"
        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": "",
            "prop": "coordinates"
        }
        allWereFound = 1
        for label in self.allLabels:
            if label not in data.allLabels:
                print("label"+label+"not in data")
                allWereFound = 0
            else:
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
                        with open('output/' + toFilename(label) + '.json', 'r', encoding='utf-8') as read_file:
                            savedData = json.load(read_file)
                        print(doc)
                        print(savedData)
                        print(doc == savedData)
        print("allWereFound(dataTest): ", allWereFound)

    # This test is for the eyes: prints the data the way it is saved in our project and
    # we can see in the eyes that this is the same as in the partial data files.
    def test2(self):
        for label in self.allLabels:
            url = self.labelsToUrls[label]
            abstract = ""
            if url in self.urlsToAbstract:
                abstract = self.urlsToAbstract[url]
            doc = {
                "label": label,
                "url": url,
                "abstract": abstract
            }
            print(doc)



# This test make sure every coordinated label found in our final data
# 'someLabels' is list of coordinated labels, this test print "all were found:  True" at the end in case of success.
# in this case: for every label in 'someLabels' it's print all the data the script kept for this label.
def locationTest(data):
    someLabels = ["הקרב על גבעת התחמושת", "בית הספר לשוטרים (ירושלים)", "בית הספר רנה קסין",
                  "קריית הממשלה (מזרח ירושלים)", "שכונות הבריח", "קריית הלאום", "יד הזיכרון למגיני ירושלים",
                  "הרי יהודה", "סנהדריה המורחבת", "ישיבת תפארת צבי", "ישיבת מיר", "נחל צופים", "נבי סמואל",
                  "שדרות בר-לב",
                  "גן העצמאות (ירושלים)", "דרך שכם", "קבר רחל", "תחנת הרכבת ההיסטורית של ירושלים", "פארק אירופה",
                  "דיסנילנד פריז"]
    counter = 0
    for label in someLabels:
        if label in data.allLabels:
            counter += 1
            with open('output/' + toFilename(label) + '.json', 'r', encoding='utf-8') as read_file:
                savedData = json.load(read_file)
                print(savedData)
    print("all were found(locationTest): ", counter == someLabels.__len__())


def toFilename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


class dataLoad:
    def __init__(self):
        # data structures
        self.allLabels = []
        self.labelsToUrls = {}
        self.urlsToAbstract = {}

        # get data
        self.__labelsAndUrlsFromJson()
        self.__abstractsFromJson()
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
            url = urllib.parse.unquote(abstractDict['uri'])
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
                # with open('output/' + toFilename(doc["label"]) + '.json', 'w', encoding='utf-8') as outfile: #for saving the files on your computer
                #     json.dump(doc, outfile, ensure_ascii=False)
                docs.append(doc)
    return docs


def elasticBuilder(elasticDocs):
    for doc in elasticDocs:
        print("start indexing label " + doc["label"] + "...")
        res = S.post(url='http://localhost:9200/nerya/_doc/' + doc["label"],
                     headers={'Content-Type': 'application/json'}, json=doc)
        print("start indexing label " + doc["label"] + "...")


# def search(distance, latLonPoint):
#     PARAMS = {
#         "filtered": {search("12km", "40,-70")
#             "query": {
#                 "match_all": {}
#             },
#             "filter": {
#                 "geo_distance": {
#                     "distance": distance,
#                     "doc.coordinates": latLonPoint
#                 #                       example
#                 #                     "distance" : "12km"
#                 #                     "doc.coordinates" : "40,-70"
#                 #                     https: // github.com / elastic / elasticsearch / issues / 279
#                 }
#             }
#         }
#     }
#
#
# def sortSearch(distance, latLonLocation):
#     PARAMS = {
#         "sort": [
#             {
#                 "_geo_distance": {
#                     "doc.coordinates": latLonLocation,
#                     "order": "asc",  # ascending order
#                     "unit": "km"
#                 }
#             }
#         ],
#         "query": {
#             "match_all": {}
#         }
#     }
#

def main():
    data = dataLoad()

    locationTest(data)
    t = dataTest()
    t.test2()
    t.test1(data)

    elasticDocs = saveWithCoordinates(data)
    elasticBuilder(elasticDocs)
    # search("12km", "40,-70")


if __name__ == "__main__":
    main()
