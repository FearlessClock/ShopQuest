class Node:
    """Node structure to represent the graph of the maze. Allows us to know a lot of information about the maze in one position"""

    def __init__(self, pos, wall):
        self.pos = pos
        self.floor = 0
        self.icon = None
        self.wall = wall
        self.payload = 0
        self.neighbors = []
        self.parent = None
        self.g = -1
        self.f = -1

    def setIcon(self, iconImage):
        self.icon = iconImage

    def addNeighbors(self, node):
        self.neighbors.append(node)

    def removeNeighbors(self, node):
        self.neighbors.remove(node)

    def getPayload(self):
        return self.payload

    def setPayload(self, val):
        self.payload = val

    def getNeighbors(self):
        return self.neighbors


