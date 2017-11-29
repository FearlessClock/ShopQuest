# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:14:25 2017

@author: piete
"""
try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def posArray(self):
        return [self.x, self.y]


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


class Creature:
    def __init__(self, x, y, color):
        self.pos = Vector(x, y)
        self.color = color

    def drawCreature(self, screen, stepSize):
        curRect = (self.pos.x * stepSize + 2, self.pos.y * stepSize + 2, stepSize - 2, stepSize - 2)
        pygame.draw.rect(screen, self.color, curRect, 0)

    def isOnItem(self, maze):
        x = self.pos.x
        y = self.pos.y
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload == 2:
            return True;
        return False;

    @staticmethod
    def checkEmpty(x, y, maze):
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload != 1:
            return True
        return False


class Player(Creature):
    def __init__(self, x, y, color):
        Creature.__init__(self, x, y, color)

        self.up = 273
        self.down = 274
        self.right = 275
        self.left = 276

        self.speed = 1

    def move(self, key, maze):
        if key == self.up and self.checkEmpty(self.pos.x, self.pos.y - 1, maze):
            self.pos.y -= self.speed
        elif key == self.down and self.checkEmpty(self.pos.x, self.pos.y + 1, maze):
            self.pos.y += self.speed
        elif key == self.left and self.checkEmpty(self.pos.x - 1, self.pos.y, maze):
            self.pos.x -= self.speed
        elif key == self.right and self.checkEmpty(self.pos.x + 1, self.pos.y, maze):
            self.pos.x += self.speed


def distanceToNode(start, goal):
    return math.sqrt(math.pow(start.pos.x - goal.pos.x, 2) + math.pow(start.pos.y - goal.pos.y, 2))


def reconstructPath(node):
    path = []
    while node.parent != None:
        path.append(node)
        node = node.parent
    return path


def GetHScore(curNeigh, goal):
    return distanceToNode(curNeigh, goal)


def getRandomFloorValue():
    return random.randint(0, 10)


class AI(Creature):
    def __init__(self, x, y, color):
        Creature.__init__(self, x, y, color)
        self.pos = Vector(x, y)
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
            sorted(openSet, key=lambda Node: Node.f)
            current = openSet.pop(0)
            if current == goal:
                return reconstructPath(current)

            closedSet.append(current)

            neighs = current.getNeighbors()
            for i in range(0, len(neighs)):
                if len(neighs) > 0 and random.random() > 0.9:
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


def mapToRange(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


def showScreen(screen, maze):
    # Display the map
    stepSize = width / len(maze)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            curRect = (i * stepSize + 1, j * stepSize + 1, stepSize - 1, stepSize - 1)
            payload = maze[i][j].payload
            if payload == 1:
                pygame.draw.rect(screen, (255, 0, 0), curRect, 0)
            elif payload == 0:
                val = math.fabs(maze[i][j].f)*5
                if val > 254:
                    val = 254
                pygame.draw.rect(screen, (val, 255, val), curRect, 0)
            elif payload == 2:
                pygame.draw.rect(screen, (255, 100, 0), curRect, 0)


def getRandomEmptyBlock(maze):
    itemPos = Vector(random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1))
    while maze[itemPos.x][itemPos.y].payload == 1:
        itemPos = Vector(random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1))
    return itemPos


def readMaze():
    # Read the file containing the maze
    f = open('maze.txt', 'r')
    N = int(f.readline())
    maze = []
    for i in range(N):
        maze.append([])
        for j in range(N):
            maze[i].append(Node(Vector(i, j), 0))
    for i in range(N):
        fileRead = f.readline().split()
        for j in range(len(fileRead)):
            maze[j][i].payload = int(fileRead[j])
    for i in range(N):
        for j in range(len(fileRead)):
            if j + 1 < N and not isWall(maze, j + 1, i):
                maze[j][i].neighbors.append(maze[j + 1][i])
            if j - 1 >= 0 and not isWall(maze, j - 1, i):
                maze[j][i].neighbors.append(maze[j - 1][i])
            if i + 1 < N and not isWall(maze, j, i + 1):
                maze[j][i].neighbors.append(maze[j][i + 1])
            if i - 1 >= 0 and not isWall(maze, j, i - 1):
                maze[j][i].neighbors.append(maze[j][i - 1])
    f.close()
    itemPos = getRandomEmptyBlock(maze)
    maze[itemPos.x][itemPos.y].payload = 2
    return width / len(maze), N, maze, itemPos


def isWall(maze, x, y):
    if maze[x][y].payload != 1:
        return False
    return True


width = 400
height = 400


def main():
    score = 0
    player = Player(1, 15, (0, 0, 255))
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    stepSize, N, maze, itemPos = readMaze()
    ai = AI(1, 3, (255, 0, 255))
    showScreen(screen, maze)
    player.drawCreature(screen, stepSize)
    pygame.display.update()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYUP:
                player.move(event.key, maze)
                showScreen(screen, maze)
                player.drawCreature(screen, stepSize)
                # ai.moveInDirection(random.randint(0, 3), maze)
                ai.moveToNode(maze, maze[itemPos.x][itemPos.y])
                if ai.isOnItem(maze):
                    maze[ai.pos.x][ai.pos.y].payload = 0
                    itemPos = getRandomEmptyBlock(maze)
                    maze[itemPos.x][itemPos.y].payload = 2
                if player.isOnItem(maze):
                    maze[player.pos.x][player.pos.y].payload = 0
                    score += 1
                    print score
                    itemPos = getRandomEmptyBlock(maze)
                    maze[itemPos.x][itemPos.y].payload = 2
                    ai.path = []
                ai.drawCreature(screen, stepSize)
                pygame.display.update()


if __name__ == '__main__': main()
