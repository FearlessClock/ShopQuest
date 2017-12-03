class Node:
    def __init__(self, pos, payload):
        self.pos = pos
        self.floor = 0
        self.payload = payload
        self.neighbors = []
        self.parent = None
        self.g = -1
        self.f = -1

    def addNeighbors(self, node):
        self.neighbors.append(node)

    def removeNeighbors(self, node):
        self.neighbors.remove(node)

    def getPayload(self):
        return self.payload

    def getNeighbors(self):
        return self.neighbors


