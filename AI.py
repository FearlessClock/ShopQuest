import Creature
import Vector
import math
import random


def distanceToNode(start, goal):
    return math.sqrt(math.pow(start.pos.x - goal.pos.x, 2) + math.pow(start.pos.y - goal.pos.y, 2))


def GetHScore(curNeigh, goal):
    return distanceToNode(curNeigh, goal)


def reconstructPath(node):
    path = []
    while node.parent is not None:
        path.append(node)
        node = node.parent
    return path



class AI(Creature.Creature):
    def __init__(self, x, y, color, filename, tileSize):
        Creature.Creature.__init__(self, x, y, color, filename, tileSize)
        self.pos = Vector.Vector(x, y)
        self.path = []

    def moveInDirection(self, direction, maze):
        if direction == 0:
            if self.pos.x - 1 > 0:
                if self.checkEmpty(self.pos.x - 1, self.pos.y, maze):
                    self.pos.x -= 1
        elif direction == 1:
            if self.pos.y - 1 > 0:
                if self.checkEmpty(self.pos.x, self.pos.y - 1, maze):
                    self.pos.y -= 1
        elif direction == 2:
            if self.pos.x + 1 < len(maze):
                if self.checkEmpty(self.pos.x + 1, self.pos.y, maze):
                    self.pos.x += 1
        elif direction == 3:
            if self.pos.y + 10 < len(maze):
                if self.checkEmpty(self.pos.x, self.pos.y + 1, maze):
                    self.pos.y += 1

    def moveToNode(self, maze, goal):
        if len(self.path) == 0:
            self.path = self.aStar(maze, maze[self.pos.x][self.pos.y], goal)
        if len(self.path) > 0:
            self.pos = self.path.pop().pos
        else:
            self.moveInDirection(random.randint(0, 4), maze)

    def aStar(self, maze, start, goal):
        # Already visited nodes
        for i in range(0, len(maze)):
            for j in range(0, len(maze)):
                maze[i][j].g = -1
                maze[i][j].f = 0
                maze[i][j].parent = None
                maze[i][j].floor = 0

        closedSet = []

        start.g = 0
        start.f = distanceToNode(start, goal)

        # Possible nodes to visit
        openSet = [start]

        while len(openSet) > 0:
            index = 0
            best = openSet[index].f
            for i in range(0, len(openSet)):
                if openSet[i].f < best:
                    best = openSet[i].f
                    index = i
            current = openSet.pop(index)
            if current == goal:
                return reconstructPath(current)

            closedSet.append(current)

            neighs = current.getNeighbors()
            for i in range(0, len(neighs)):
                if len(neighs) > 0 and random.random() > 0.95:
                    continue
                curNeigh = neighs[i]
                if closedSet.__contains__(curNeigh):
                    continue

                if not openSet.__contains__(curNeigh):
                    openSet.append(curNeigh)

                tentativeGScore = current.g + 1
                if curNeigh.g != -1 and tentativeGScore >= curNeigh.g:
                    continue  # It's not a better score

                curNeigh.parent = current
                curNeigh.g = tentativeGScore
                curNeigh.f = curNeigh.g + GetHScore(curNeigh, goal)
                curNeigh.floor = 255
        print "Error No path found"
        return []
