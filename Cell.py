'''
Cell class used to represent each part of the maze
'''
class Cell(object):

    '''
    Constructor for the Cell class
    @brief Create a cell with information about position, walls and visited state
    @param coordX   The X position of the cell
    @param coordY   The Y position of the cell
    '''
    def __init__(self, coordX, coordY):
        self.coordY = coordY
        self.coordX = coordX
        self.visited = False
        self.walls = {"TOP": True, "RIGHT": True, "BOTTOM": True, "LEFT": True}

    '''
    Function removing a wall between two cells based on the coord of the given neighbour cell
    @param neighbour_coordX   The X position of the neighbour
    @param neighbour_coordY   The Y position of the neighbour
    '''
    def removeWalls(self, neighbour_coordX, neighbour_coordY):
        if (self.coordX - neighbour_coordX == 1):
            self.walls["TOP"] = False
        elif (self.coordX - neighbour_coordX == -1):
            self.walls["BOTTOM"] = False
        elif (self.coordY - neighbour_coordY == 1):
            self.walls["LEFT"] = False        
        elif (self.coordY - neighbour_coordY == -1):
           self.walls["RIGHT"] = False
            