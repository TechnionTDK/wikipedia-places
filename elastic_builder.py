import requests
import json

allLabels = []
labelsToUrls = {}
labelsToCoordinates = {}

# loading data
with open(r"input/wiki_hebrew_labels.json", "r", encoding='utf-8') as read_file:
    labelsAndUrls = json.load(read_file)


for labelDict in labelsAndUrls:
    label = labelDict['rdfs:label']
    allLabels.append(label)
    labelsToUrls[label] = labelDict['uri']
print(allLabels.__len__())
# print(labelsToUrls)
# print(labels[labels.__len__()-1])
# print(urls[urls.__len__()-1])


# with open(r"input/wiki_hebrew_abstracts.json", "r", encoding='utf-8') as read_file:
#     data = json.load(read_file)
# print(data)



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
            labelsToCoordinates[label] = v['coordinates'][0]
            # print("Latitute: " + str(v['coordinates'][0]['lat']))
            # print("Longitude: " + str(v['coordinates'][0]['lon']))
        else:
            del labelsToUrls[label]

print("#coordinatesSize: ", labelsToCoordinates.__len__())
print("#urlsSize: ", labelsToUrls.__len__())

testLabel = allLabels[allLabels.__len__()-1]
print(testLabel, labelsToCoordinates[testLabel], labelsToUrls[testLabel])

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
