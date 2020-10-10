import requests
from elasticsearch import Elasticsearch
S = requests.Session()
index = "all"


def connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def test():
    # init
    someAreas = ["10m, 31.799017, 35.22808", "50m, 31.79, 35.22", "10000m, 31.79, 35", "8000m, 32, 34", "800m, 31.7, 35.2",
                   "5000m, 31.8, 35.16", "1000m, 31.8, 35.21", "500m, 31.6667, 35.16667", "100m, 31.80472, 35.22222",
                 "1000m, 32, 35", "1000m, 50, 11", "1220m, 43.25, -2.92", "80m, 47, 2.4", "2000m, 44, 0", "500m, 42, -3",
                 "2200m, 49, 1", "1000m, 48, 2", "500m, 40, -1", "20m, 42, 12", "1500m, 44, 24", "10m, -20, 60"]

    basicTest = ["10m, 31.799017, 35.22808", "50m, 31.79, 35.22", "1000m, 50, 11", "80m, 47, 2.4",
                 "1000m, 48, 2", "500m, 40, -1", "20m, 42, 12", "50m, -20, 60"]

    base = someAreas


    # run
    for area in base:
        elasticRes = elasticSearch(area)
        success = Geosearch(area, elasticRes)
        print("success of " + area + ":", success)
        if not success:
            return 0
    return 1



def compare(geoPlace, elasticFull):
    if len(elasticFull) == 500:
        print("fullSize")
        return 1
    geoTitle = geoPlace['title']
    for data in elasticFull:
        relevant = data["_source"]
        location = relevant["pin"]["location"]
        title = relevant["label"]
        if title == geoTitle:
            print("title were found: " + geoTitle)
            return round(geoPlace["lat"],8) == round(location["lat"],8) and round(geoPlace["lon"],8) == round(location["lon"],8)
    print("title weren't found: " + geoTitle)
    return 0


def Geosearch(params, elasticRes):
    print("in geo------------------------")
    params = params.split(', ')
    gsradius = params[0].split('m')[0]
    URL = "https://he.wikipedia.org/w/api.php"
    # parameter "gsradius" must be between 10 and 10,000
    PARAMS = {
        "format": "json",
        "list": "geosearch",
        "gscoord": params[1]+"|"+params[2],
        "gslimit": "500",
        "gsradius": gsradius,
        "action": "query"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    print(DATA)
    PLACES = DATA['query']['geosearch']
    if len(PLACES)!=len(elasticRes):
        print("len(geoPlace)!=len(elasticRes): ",len(PLACES), "!=", len(elasticRes))
        return 0

    # geoPlaces = []
    # for place in PLACES:
    #     geoPlaces.append(place['title'])
    # geoPlaces.sort()
    # print(len(geoPlaces))
    # for i in range(len(geoPlaces)):
    #     print("geo: ",geoPlaces[i],", elastic: ",elasticRes[i]["_source"]["label"])

    for place in PLACES:
        if not compare(place, elasticRes):
            return 0
        print("compare of "+place['title']+" is good")
    return 1
        # print(place)
        # print(place['title'])
    # print("total hits in Geo: ", len(PLACES))


def elasticSearch(params):
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
    res = elastic_client.search(index=index, body=query, size=500)
    print("Elastic: ", res)
    # print("total hits with Elastic: ", len(res["hits"]["hits"]))
    return res["hits"]["hits"]


def main():
    print("Total test: success if 1 ==", test())


if __name__ == "__main__":
    main()
