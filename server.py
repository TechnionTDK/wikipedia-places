
from flask import Flask, request
import json
# instantiate the app
from search import search

app = Flask(__name__)

@app.route("/wiki_by_place")
def RUN_SEARCH():
    params = []
    params.append(request.args.get('radius', type=str))
    params+=request.args.get('lat,lon', type=str).split(",")
    return json.dumps(search(params), ensure_ascii=False)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='80')

""" HTML  request would be
http://132.69.8.7/wiki_by_place?radius=xxx&lat=xxx&lon=xxx
example:
http://132.69.8.7/wiki_by_place?radius=1km&lat=32.7775&lon=35.02166667
"""

