from flask import Flask 
from flask import request, jsonify
from .graph.Graph import Graph, Node, distance, dijkstra, nearest, bearing

app = Flask(__name__)
app.config["DEBUG"] = True

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
# http://127.0.0.1:5000/api/path?lat=33.64307&lon=-84.43250&airport=yyz&map=2&destID=C55

# tutorial
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

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
    numVertices = 6
    graph = Graph(numVertices)

    node1 = Node(1, 33.64331, -84.43274, "C52")
    node2 = Node(2, 33.64331, -84.43252, "C55")
    node3 = Node(3, 33.64329, -84.43284, "C50")
    node4 = Node(4, 33.64310, -84.43282, "C46")
    node5 = Node(5, 33.64311, -84.43241, "C49")

    # need to query from db to determine the node num of the dest id
    # rn this is hardcoded
    destination = 1
    destNode = node1

    # add vertices
    graph.addVertex(node1)
    graph.addVertex(node2)
    graph.addVertex(node3)
    graph.addVertex(node4)
    graph.addVertex(node5)

    # add directed edges
    # direction is in degrees north
    graph.addEdge(node1, node2)
    graph.addEdge(node2, node1)
    graph.addEdge(node2, node5)
    graph.addEdge(node5, node2)
    graph.addEdge(node3, node1)
    graph.addEdge(node1, node3)
    graph.addEdge(node4, node5)
    graph.addEdge(node5, node4)
    graph.addEdge(node3, node4)
    graph.addEdge(node4, node3)

    # graph.printGraph()

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

