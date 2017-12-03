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
    import Vector
    import Player
    import AI
    import Node
    from socket import *
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


def getRandomFloorValue():
    return random.randint(0, 10)


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
                val = math.fabs(maze[i][j].f) * 5
                if val > 254:
                    val = 254
                pygame.draw.rect(screen, (val, 255, val), curRect, 0)
            elif payload == 2:
                pygame.draw.rect(screen, (255, 100, 0), curRect, 0)


def getRandomEmptyBlock(maze):
    itemPos = Vector.Vector(random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1))
    while maze[itemPos.x][itemPos.y].payload == 1:
        itemPos = Vector.Vector(random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1))
    return itemPos


def readMaze():
    # Read the file containing the maze
    f = open('maze.txt', 'r')
    N = int(f.readline())
    maze = []
    fileRead = ""
    for i in range(N):
        maze.append([])
        for j in range(N):
            maze[i].append(Node.Node(Vector.Vector(i, j), 0))
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
    player = Player.Player(1, 15, (0, 0, 255))
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    stepSize, N, maze, itemPos = readMaze()
    ai = AI.AI(1, 3, (255, 0, 255))
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
