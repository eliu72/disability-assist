from flask import Flask 
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from .graph.Graph import Graph, Node, distance, dijkstra, nearest, bearing
import json, os

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# running virtual environment on windows
###############################################
# virtualenv env
# .\env\Scripts\activate.bat
# python app.py
# flask run

# deploy to heroku
###############################################
# git add .
# git commit -m "mesg"
# git push
# git push heroku main

# Local Testing Params
###############################################
# http://127.0.0.1:5000/api/path?lat=33.64307&lon=-84.43250&airport=ATL&map=C&destID=C55

# BUILDING A PYTHON FLASK API TUTORIAL
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

# DEPLOYING TO HEROKU TUTORIAL
# https://dev.to/techparida/how-to-deploy-a-flask-app-on-heroku-heb 
# Reference Only: https://stackabuse.com/deploying-a-flask-application-to-heroku/
# Reference Only: https://realpython.com/flask-by-example-part-1-project-setup/

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Disability Assistance API</h1>
<p>A prototype API for retrieving directions for airport navigation.</p>'''

@app.route('/api/path', methods=['GET'])
def api_all():

    query_parameters = request.args
    
    # user geo location
    lat = float(query_parameters.get('lat'))
    lon = float(query_parameters.get('lon'))

    # requested map
    airport = query_parameters.get('airport')
    myMap = query_parameters.get('map')

    # requested destination id  - ex. "C52", "C55", etc
    destID = query_parameters.get('destID')

    # init digraph
    numVertices = 61
    graph = Graph(numVertices)

    # graph to load
    MYDIR = os.path.dirname(__file__)
    filename = "maps/" + airport + "/" + myMap + ".json"
    
    with open(os.path.join(MYDIR, filename)) as f:
        data = json.load(f)
    
    # create graph
    for i in data:

        # add vertex to graph
        node = Node(i["label"], float(i["lat"]), float(i["lon"]), i["name"])
        graph.addVertex(Node(i["label"], float(i["lat"]), float(i["lon"]), i["name"]))
        
        # determine adjacencies and add edges
        adjacentNodes = i["neighbors"]
        for j in adjacentNodes:
            adjNode = Node(j, data[j-1]["lat"], data[j-1]["lon"], data[j-1]["name"])
            graph.addEdge(node, adjNode)

    # need to query from db to determine the node num of the dest id
    filename = "maps/" + airport + "/" + myMap + "_places.json"
    with open(os.path.join(MYDIR, filename)) as f:
        data_places = json.load(f)
    destination = int(data_places[destID])
    destNode = graph.getVertex(destination)
    print(destination)

    # search for the shortest path from curr location to destination
    nearestNode, dist, direction = nearest(numVertices, graph, lat, lon, "M")
    paths = dijkstra(numVertices, graph, destNode)
    paths[0] = nearestNode.getLabel()

    print(paths)

    # list of vertices
    vertices = graph.getVertices()

    # json output for the legs of the route
    legs = []

    # current start node
    startNode = 0

    # current destination node
    destNode = paths[startNode]

    # add the path from curr location to nearest node
    i = 1
    currLeg = {}
    currLeg["leg"] = i
    currLeg["start"] = {"lat": lat, "lon": lon}
    currLeg["end"] = {"lat": vertices[destNode].getLat(), "lon": vertices[destNode].getLon()}
    currLeg["distance"] = {"miles": dist}
    currLeg["direction"] = {"degrees": direction, "bearing": "degrees from east"}


    legs.append(currLeg)
    
    i += 1

    startNode = destNode

    # add remaining paths
    while paths[startNode] != None:

        # update destination node
        destNode = paths[startNode]

        # build the path for the current leg
        currLeg = {}
        currLeg["leg"] = i
        currLeg["start"] = {"lat": vertices[startNode].getLat(), "lon": vertices[startNode].getLon()}
        currLeg["end"] = {"lat": vertices[destNode].getLat(), "lon": vertices[destNode].getLon()}
        currLeg["distance"] = {"miles": distance(vertices[startNode], vertices[destNode])}
        currLeg["direction"] = {"degrees": bearing(vertices[startNode], vertices[destNode]), "bearing": "degrees from east"}

        # append to list of legs
        legs.append(currLeg)
        startNode = destNode
        i += 1

    return jsonify(legs)

@app.route('/api/places', methods=['GET'])
def api_places():
    
    query_parameters = request.args
    
    # requested map
    airport = query_parameters.get('airport')
    myMap = query_parameters.get('map')

    # places to load
    MYDIR = os.path.dirname(__file__)
    filename = "maps/" + airport + "/" + myMap + "_places.json"
    with open(os.path.join(MYDIR, filename)) as f:
        data = json.load(f)
    
    return jsonify(data)
