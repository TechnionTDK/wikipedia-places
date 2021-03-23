
from elasticsearch import Elasticsearch
import geopy.distance
index = "all"


def connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def search(params):
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
    res = elastic_client.search(index=index, body=query, size=10000)
    sourceCoords = (float(params[1]), float(params[2]))
    withDist = []
    for data in res["hits"]["hits"]:
        relevant = data["_source"]

        location = relevant["pin"]["location"]
        curCoords = (location["lat"], location["lon"])
        dist = geopy.distance.distance(sourceCoords, curCoords).km
        relevant["pin"]["distance[km]"] = dist

        withDist.append(relevant)
    return withDist


def main():
    #example:
    params = "1km, 32.7775, 35.02166667".split(", ")
    print(search(params))


if __name__ == "__main__":
    main()
