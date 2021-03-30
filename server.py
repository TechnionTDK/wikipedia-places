
from flask import Flask, request
import json
from search import search

# instantiate the app
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

""" HTML request would be
http://132.69.8.7/wiki_by_place?radius=xxx&lat,lon=xxx,xxx  
http://132.69.8.7/wiki_by_place?lat,lon=xxx,xxx&radius=xxx  
Examples - up to 1km from the Technion:  
http://132.69.8.7/wiki_by_place?radius=1km&lat,lon=32.7775,35.02166667  
http://132.69.8.7/wiki_by_place?radius=1000m&lat,lon=32.7775,35.02166667  
http://132.69.8.7/wiki_by_place?lat,lon=32.7775,35.02166667&radius=100000cm  
"""

