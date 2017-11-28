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
        self.payload = payload
        self.neighbors = []
        self.parent = None
        self.g = -1
        self.h = -1
        self.f = -1

    def AddNeighbors(self, node):
        self.neighbors.append(node)

    def RemoveNeighbors(self, node):
        self.neighbors.remove(node)

    def GetPayload(self):
        return self.payload


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


class AI(Creature):
    def __init__(self, x, y, color):
        Creature.__init__(self, x, y, color)
        self.pos = Vector(x, y)

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

    def distanceToNode(self, start, goal):
        return math.sqrt(math.pow(start.x - goal.x, 2),math.pow(start.y - goal.y, 2) )

    def AStart(self, maze, start, goal):
        #Already visited nodes
        closedSet = []

        start.g = 0
        start.f = self.distanceToNode(start, goal)

        #Possible nodes to visit
        openSet = [start]

        while len(openSet) > 0:
            sorted(openSet, key=lambda Node: Node.f)
            current = openSet.pop(0)

        '''
    while openSet is not empty
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)

        openSet.Remove(current)
        closedSet.Add(current)

        for each neighbor of current
            if neighbor in closedSet
                continue		// Ignore the neighbor which is already evaluated.

            if neighbor not in openSet	// Discover a new node
                openSet.Add(neighbor)
            
            // The distance from start to a neighbor
            //the "dist_between" function may vary as per the solution requirements.
            tentative_gScore := gScore[current] + dist_between(current, neighbor)
            if tentative_gScore >= gScore[neighbor]
                continue		// This is not a better path.

            // This path is the best until now. Record it!
            cameFrom[neighbor] := current
            gScore[neighbor] := tentative_gScore
            fScore[neighbor] := gScore[neighbor] + heuristic_cost_estimate(neighbor, goal) 

    return failure

function reconstruct_path(cameFrom, current)
    total_path := [current]
    while current in cameFrom.Keys:
        current := cameFrom[current]
        total_path.append(current)
    return total_path
        '''

def showScreen(screen, maze):
    # Display the map
    stepSize = width / len(maze)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            curRect = (i * stepSize + 1, j * stepSize + 1, stepSize - 1, stepSize - 1)
            payload = maze[i][j].payload
            print payload
            if payload == 1:
                pygame.draw.rect(screen, (255, 0, 0), curRect, 0)
            elif payload == 0:
                pygame.draw.rect(screen, (0, 255, 0), curRect, 0)
            elif payload == 2:
                pygame.draw.rect(screen, (255, 100, 0), curRect, 0)


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
    f.close()
    return width / len(maze), N, maze


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

    stepSize, N, maze = readMaze()
    ai = AI(2, 3, (255, 0, 255))
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
                if player.isOnItem(maze):
                    maze[player.pos.x][player.pos.y].payload = 0
                    score += 1
                    print score
                    maze[random.randint(0, N - 1)][random.randint(0, N - 1)].payload = 2
                showScreen(screen, maze)
                player.drawCreature(screen, stepSize)
                ai.moveInDirection(random.randint(0, 3), maze)
                if ai.isOnItem(maze):
                    maze[ai.pos.x][ai.pos.y].payload = 0
                    maze[random.randint(0, N - 1)][random.randint(0, N - 1)].payload = 2
                ai.drawCreature(screen, stepSize)
                pygame.display.update()


if __name__ == '__main__': main()
