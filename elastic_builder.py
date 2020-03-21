import requests
import json

allLabels = []
labelsToUrls = {}
#labelsToCoordinates = {}
urlsToAbstract = {}
elasticDocs = {}

# loading data
with open(r"input/wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
    labelsAndUrls = json.load(read_file)
with open(r"input/wiki_hebrew_abstracts.json", "r", encoding='utf-8') as read_file:
    abstractsAndUrls = json.load(read_file)

for labelDict in labelsAndUrls:
    label = labelDict['rdfs:label']
    allLabels.append(label)
    labelsToUrls[label] = labelDict['uri']

for abstractDict in abstractsAndUrls:
    url = abstractDict['uri']
    urlsToAbstract[url] = abstractDict['dbo:abstract']


# get coordinates
S = requests.Session()

URL = "https://he.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "format": "json",
    "titles": "",
    "prop": "coordinates"
}


# allLabels = ["הקרב על גבעת התחמושת", "בית הספר לשוטרים (ירושלים)", "בית הספר רנה קסין", "קריית הממשלה (מזרח ירושלים)", "שכונות הבריח", "קריית הלאום", "יד הזיכרון למגיני ירושלים",
#           "הרי יהודה", "סנהדריה המורחבת", "ישיבת תפארת צבי", "ישיבת מיר", "נחל צופים", "נבי סמואל", "שדרות בר-לב",
#           "גן העצמאות (ירושלים)", "דרך שכם", "קבר רחל", "תחנת הרכבת ההיסטורית של ירושלים", "פארק אירופה", "דיסנילנד פריז"]



for label in allLabels:
    PARAMS["titles"] = label
    for k, v in S.get(url=URL, params=PARAMS).json()['query']['pages'].items():
        if 'coordinates' in v:
            fullCoordinates = v['coordinates'][0]
            coordinates = {
                "lat": fullCoordinates['lat'],
                "lon": fullCoordinates['lon']
            }
            url = labelsToUrls[label]
            doc = {
                "label": label,
                "coordinates": coordinates,
                "url": url,
                "abstract": urlsToAbstract[url]
            }
            elasticDocs.append(doc)
            # print("Latitute: " + str(v['coordinates'][0]['lat']))
            # print("Longitude: " + str(v['coordinates'][0]['lon']))
        # else:
        #     del labelsToUrls[label]
# print(labelsToCoordinates)
# print("#coordinatesSize: ", labelsToCoordinates.__len__())
# print("#urlsSize: ", labelsToUrls.__len__())
#
# testLabel = allLabels[allLabels.__len__()-1]
# print(testLabel, labelsToCoordinates[testLabel])
for doc in elasticDocs:
    with open('output/' + doc["label"] + '.json', 'w', encoding='utf-8') as outfile:
        json.dump(doc, outfile, ensure_ascii=False)
    res = S.post(url='http://localhost:9200/nerya/_doc/'+doc["label"], headers={'Content-Type': 'application/json'}, json=doc)

# for label in allLabels:p
#     elas_doc = {
#         "label": label,
#         "coordinates": labelsToCoordinates[label]
#     }
#
#     # es.index(index="nerya", doc_type='_doc', id=label,body=doc)
#     print("start indexing lable "+label+ "...")
#     res = S.post(url='http://localhost:9200/nerya/_doc/'+label, headers={'Content-Type': 'application/json'}, json=elas_doc)
#     print("finished indexing lable "+label+"!")



# for label in labels:
#     if label not in results:
#         print(label)



# code example:
# R = S.get(url=URL, params=PARAMS)
# DATA = R.json()
# PAGES = DATA['query']['pages']
# print(PAGES.items())
# print(PAGES.items)
# for k, v in PAGES.items():


# ירושלים info:
# dict_items([('325', {'pageid': 325, 'ns': 0, 'title': 'ירושלים', 'coordinates': [{'lat': 31.78264861, 'lon': 35.2193299, 'primary': '', 'globe': 'earth'}]})])
