
class Cell(object):

    def __init__(self, coordX, coordY):
        self.coordY = coordY
        self.coordX = coordX
        self.visited = False
        self.walls = {"TOP": True, "RIGHT": True, "BOTTOM": True, "LEFT": True}


    def removeWalls(self, neighbour_coordX, neighbour_coordY):
        if (self.coordX - neighbour_coordX == 1):
            self.walls["TOP"] = False
        elif (self.coordX - neighbour_coordX == -1):
            self.walls["BOTTOM"] = False
        elif (self.coordY - neighbour_coordY == 1):
            self.walls["LEFT"] = False        
        elif (self.coordY - neighbour_coordY == -1):
           self.walls["RIGHT"] = False
            