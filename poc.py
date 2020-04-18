import json
import re
import requests
from elasticsearch import Elasticsearch
import geopy.distance

S = requests.Session()

index = "poc"


def toFilename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def restartElasticWithoutAll():
    es = connect()
    for i in es.indices.get('*'):
        if i != "all":
            es.indices.delete(index=i)


def restartElasticPOC():
    connect().indices.delete(index=index)


def elasticBuilder():
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
    someLabels = ["הקרב על גבעת התחמושת", "בית הספר לשוטרים (ירושלים)", "בית הספר רנה קסין",
                  "קריית הממשלה (מזרח ירושלים)", "שכונות הבריח", "קריית הלאום", "יד הזיכרון למגיני ירושלים",
                  "הרי יהודה", "סנהדריה המורחבת", "ישיבת תפארת צבי", "ישיבת מיר", "נחל צופים", "נבי סמואל",
                  "שדרות בר-לב",
                  "גן העצמאות (ירושלים)", "דרך שכם", "קבר רחל", "תחנת הרכבת ההיסטורית של ירושלים", "פארק אירופה",
                  "דיסנילנד פריז"]

    for label in someLabels:
        with open('poc/' + toFilename(label) + '.json', 'r', encoding='utf-8') as read_file:
            savedData = json.load(read_file)
            pin = {"location":
                       savedData["coordinates"]
                   }
            pin = {
                "label": savedData["label"],
                "pin": pin,
                "url": savedData["url"],
                "abstract": savedData["abstract"]
            }
            print(pin)

            res = es.index(index=index, body=pin)
            print(res)

    print("finishBuild")


def search(params):
    params = params.split(', ')
    query = {
        "query": {
            "bool": {
                "filter": {
                    "geo_distance": {
                        "distance": params[0],
                        "pin.location": {
                            "lat": params[1],
                            "lon": params[2]
                        }
                    }
                }
            }
        }
    }

    elastic_client = connect()
    res = elastic_client.search(index=index, body=query, size=199)
    print(res)
    print("total hits:", len(res["hits"]["hits"]))
    sourceCoords = (float(params[1]), float(params[2]))
    withDist = []
    for data in res["hits"]["hits"]:
        # print(data)
        relevant = data["_source"]

        location = relevant["pin"]["location"]
        curCoords = (location["lat"], location["lon"])
        dist = geopy.distance.distance(sourceCoords, curCoords).km
        relevant["pin"]["distance[km]"] = dist

        print(location)
        print(dist)
        withDist.append(relevant)
    print(withDist)


def main():
    # restartElasticPOC()
    # elasticBuilder()

    search("3km, 31.799017, 35.22808")


if __name__ == "__main__":
    main()
