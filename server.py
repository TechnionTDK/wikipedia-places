from flask import Flask, request
import json
from constants import DEFAULT_SEARCH_SIZE
from search import search
from place_details import get_place_details_by_name, get_place_details_by_coordinates, get_suggestions

# instantiate the app
app = Flask(__name__)


@app.route("/wiki_by_place")
def RUN_SEARCH():
    params = [request.args.get('radius', type=str)]
    params += request.args.get('lat,lon', type=str).split(",")
    return json.dumps(search(params, from_index=request.args.get('from', type=int, default=0), size=request.args.get('size', type=int, default=DEFAULT_SEARCH_SIZE)), ensure_ascii=False)


@app.route("/place_details_by_name")
def RUN_GET_PLACE_DETAILS_BY_NAME():
    return json.dumps(get_place_details_by_name(request.args.get('name', type=str)), ensure_ascii=False)


@app.route("/place_details_by_coordinates")
def RUN_GET_PLACE_DETAILS_BY_COORDINATES():
    return json.dumps(get_place_details_by_coordinates(lat=request.args.get('lat', type=float), lon=request.args.get('lon', type=float)), ensure_ascii=False)


@app.route("/get_suggestions")
def RUN_GET_SUGGESTIONS():
    return json.dumps(get_suggestions(request.args.get('name', type=str)), ensure_ascii=False)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='80')
