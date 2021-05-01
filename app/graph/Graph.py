import math
import heapq
import json

# running virtual environment on windows
###############################################
# virtualenv env
# .\env\Scripts\activate.bat
# python Graph.py

class Node:
    def __init__(self, label, latitude, longitude, name, distance=None, nextNode=None, dir=None):
        self.vertex = label
        self.longitude = longitude
        self.latitude = latitude
        self.dist = distance
        self.next = nextNode
        self.name = name
        self.dir = dir
    
    def printNode(self):
        print("(" + str(self.vertex) + ") " + self.name + ": " + str(self.latitude) + ", " + str(self.longitude))

    def getName(self):
        return self.name

    def getLon(self):
        return self.longitude
    
    def getLat(self):
        return self.latitude
    
    def getDist(self):
        return self.dist
    
    def getLabel(self):
        return self.vertex
    
    def getNext(self):
        return self.next
    
    def setNext(self, nextNode):
        self.next = nextNode
    
    def setDist(self, dist):
        self.dist = dist
    
    def setDir(self, dir):
        self.dir = dir

class Graph:
    def __init__(self, numVertices):
        self.numVert = numVertices
        self.graph = [None] * self.numVert
        self.vertices = [None] * self.numVert

    def addEdge(self, src, dst):
        srcNode = src.getLabel()

        # calculate distance between 2 nodes
        dist = distance(src, dst)
        dst.setDist(dist)

        # calculate bearing between 2 nodes
        direction = bearing(src, dst)
        dst.setDir(direction)

        if self.graph[srcNode] == None:
            self.graph[srcNode] = []
        self.graph[srcNode].append(dst)
    
    def addVertex(self, node):
        self.vertices[node.getLabel()] = node
    
    def printGraph(self):
        for i in range(self.numVert):
            print(str(i) + ": ")
            if self.graph[i] != None:
                for j in range(len(self.graph[i])):
                    curr = self.graph[i][j]
                    print("(" + str(curr.getLabel()) + ", " + str(curr.getLat()) + ", " + str(curr.getLon()) + ", " + str(curr.getDist()) + ", " + str(curr.getName()) + ")")
    
    def getVertices(self):
        return self.vertices
    
    def getVertex(self, label):
        return self.vertices[label]
    
    def getNumVertices(self):
        return self.numVert
    
    def adjacencyList(self, currVertex):
        return self.graph[currVertex]

# calculates the bearing between two lat/lon coordiantes
# https://www.movable-type.co.uk/scripts/latlong.html
"""
Understanding bearings
------------------------
0 degrees = W
90 degrees = N
180 degrees = E
270 degrees = S
"""
def bearing(node1, node2):

    # extract lat, lon from nodes
    lat1 = node1.getLat()
    lon1 = node1.getLon()
    lat2 = node2.getLat()
    lon2 = node2.getLon()

    # calculate bearing
    y = math.sin(lon2-lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1)
    bearingRadians = math.atan2(y,x)

    # bearing in degrees
    bearing = (bearingRadians*180/math.pi + 360) % 360 

    return bearing

# calculates the distance between two lon/lat coordinates
# https://www.geodatasource.com/developers/java
def distance(node1, node2, unit="M"):

    # extract lat, lon from nodes
    lat1 = node1.getLat()
    lon1 = node1.getLon()
    lat2 = node2.getLat()
    lon2 = node2.getLon()

    # calculate distance
    if (lat1 == lat2) and (lon1 == lon2):
        return 0
    else: 
        theta = lon1-lon2
        dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
        dist = math.acos(dist)
        dist = math.degrees(dist)

        # default is miles "M"
        dist = dist * 60 * 1.1515;

        # Kilometers
        if unit == "K":
            dist = dist * 1.609344

        # Nautical miles
        elif unit == "N":
            dist = dist * 0.8684
        return dist

# given user's geolocation, determine the nearest node on the graph and distance to it
def nearest(numNodes, graph, lat, lon, unit="M"):

    vertices = graph.getVertices()
    minDist = float('inf')
    nearest = None
    direction = None

    # current geolocation
    curr = Node(0, lat, lon, "")

    for i in vertices:
        if i != None:
            dist = distance(i, curr, unit)
            if dist < minDist: 
                minDist = dist
                nearest = i 
                direction = bearing(i, curr)
    
    return nearest, minDist, direction

def dijkstra(numNodes, graph, src):
    srcNode = src.getLabel()
    
    # initialization
    distances = [float('inf')] * numNodes
    distances[srcNode] = 0
    parents = [None] * numNodes

    # init priority queue
    pq = [(0, srcNode)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        if current_distance > distances[current_vertex]:
            continue

        for node in graph.adjacencyList(current_vertex):
            distance = current_distance + node.getDist()

            # Only consider this new path if it's better than any path we've
            # already found.
            neighbor = node.getLabel()
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    return parents

# Driver program to the above graph class
if __name__ == "__main__":

    # init digraph
    numVertices = 6
    graph = Graph(numVertices)

    node1 = Node(1, 33.64331, -84.43274, "C52")
    node2 = Node(2, 33.64331, -84.43252, "C55")
    node3 = Node(3, 33.64329, -84.43284, "C50")
    node4 = Node(4, 33.64310, -84.43282, "C46")
    node5 = Node(5, 33.64311, -84.43241, "C49")

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

    graph.printGraph()

    # calculate distance between user location and nearest node
    userGeolocation = (33.64307,-84.43250)
    nearestNode, dist, bearing = nearest(numVertices, graph, userGeolocation[0], userGeolocation[1], "M")
    print()
    nearestNode.printNode()
    print(dist)
    print(bearing)

    # dijkstra
    path = dijkstra(numVertices, graph, node1)
    path[0] = nearestNode.getLabel()


    with open('../maps/ATL/C.json') as f:
        data = json.load(f)
    
    json = {}
    for i in data:
        if (i["name"] != "inter"):
            json[i["name"]] = i["label"]

    print(json)