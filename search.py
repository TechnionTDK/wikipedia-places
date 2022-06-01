import geopy.distance
import constants
import utils


def search_all(params: list) -> list:
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
    return search(query=query, params=params)


def search_pagination(params: list, from_index: int, size: int) -> list:
    query = {
        "from": from_index,
        "size": size,
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
    return search(query=query, params=params)


def search(query: dict, params: list) -> list:
    elastic_client = utils.elastic_connect()
    res = elastic_client.search(index=constants.ELASTIC_INDEX, body=query)
    source_coords = (float(params[1]), float(params[2]))
    with_dist = []
    for data in res["hits"]["hits"]:
        relevant = data["_source"]

        location = relevant["pin"]["location"]
        cur_coords = (location["lat"], location["lon"])
        dist = geopy.distance.distance(source_coords, cur_coords).km
        relevant["pin"]["distance[km]"] = dist

        with_dist.append(relevant)
    return with_dist
