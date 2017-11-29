import Cell
import random

class Maze:
    def __init__(self, width, height):
        self.width = width + 1      #Y
        self.height = height + 1    #X
        self.matrix = self.generateEmpty()
        self.visual_matrix = self.generateEmptyVisual()
        
    
    def generate(self):
        coordX = 0
        coordY = 0
        path = [(coordX, coordY)]
        self.matrix[coordX][coordY].visited = True
        visitedCount = 1
        visitedCells = list()
        
        while(visitedCount < self.height * self.width):
            currentNeighbours = self.findCurrentNeighbours(coordX, coordY)
            if(currentNeighbours is not None):
                visitedCells.append((coordX, coordY))                           #mark this position as visited
                nextCoordX, nextCoordY = random.choice(currentNeighbours)       #choose a random neighboor
                self.matrix[coordX][coordY].removeWalls(nextCoordX, nextCoordY)
                self.matrix[nextCoordX][nextCoordY].visited = True
                coordX = nextCoordX
                coordY = nextCoordY
                path.append((coordX, coordY))
                visitedCount += 1
                
            elif(len(visitedCells) > 0):
                coordX, coordY = visitedCells.pop()
                path.append((coordX, coordY)) 
                                    
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].visited = False
                                
    
    def generateEmpty(self):
        matrix = []
        for x in range(self.height):
            new = []
            for y in range(self.width):
                new.append(Cell.Cell(x, y))
            matrix.append(new)
        return matrix
    
    def generateEmptyVisual(self):
        matrix = []
        for x in range(self.height * 2 + 1):
            new = []
            for y in range(self.width * 2 + 1):
                new.append("#")
            matrix.append(new)
        return matrix
        
        
        
        
        
    def findCurrentNeighbours(self, coordX, coordY):
        neighboursList = list()
        self._findCurrentNeighbours(neighboursList, coordX - 1, coordY)  #Top
        self._findCurrentNeighbours(neighboursList, coordX, coordY + 1)  #Right
        self._findCurrentNeighbours(neighboursList, coordX + 1, coordY)  #Bottom
        self._findCurrentNeighbours(neighboursList, coordX, coordY - 1)  #Left
        
        if(len(neighboursList) > 0):
            return neighboursList
        else: 
            return None

        
    #Helper function
    def _findCurrentNeighbours(self, neighboursList, coordX, coordY):
        if (coordY >= 0 and coordY < self.width and coordX >= 0 and coordX < self.height and not self.matrix[coordX][coordY].visited):
                neighboursList.append((coordX, coordY))
        

    def updateVisualMatrix(self):
        for x in range(self.height):
            for y in range(self.width):
                self.visual_matrix[x * 2 + 1][y * 2 + 1] = "*"
                if(not self.matrix[x][y].walls["TOP"]):
                    self.visual_matrix[x * 2][y * 2 + 1] = "*"
                elif(not self.matrix[x][y].walls["RIGHT"]):
                    self.visual_matrix[x * 2 + 1][y * 2 + 2] = "*"
                elif(not self.matrix[x][y].walls["BOTTOM"]):
                    self.visual_matrix[x * 2 + 2][y * 2 + 1] = "*"
                elif(not self.matrix[x][y].walls["LEFT"]):
                    self.visual_matrix[x * 2 + 1][y * 2] = "*"

    def __str__(self):
        self.updateVisualMatrix()
        res = "" 
        for x in range(self.height * 2 + 1):
            for y in range(self.width * 2 + 1):
                res += self.visual_matrix[x][y]
            res += "\n"
        return res


maze = Maze(5,5)
maze.generate()
print maze



