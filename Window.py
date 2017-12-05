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
    import Generator
    import Node
    import Generator
    from socket import *
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


def getRandomFloorValue():
    return random.randint(0, 10)


def mapToRange(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


def showScreen(screen, maze, itemIcon):
    # Display the map
    stepSize = TILE_SIZE
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            curRect = (i * stepSize, j * stepSize, stepSize, stepSize)
            wall = maze[i][j].wall
            if wall == 1 or wall == 0:
                screen.blit(maze[i][j].icon, (curRect[0], curRect[1]))
                # pygame.draw.rect(screen, (255, 0, 0), curRect, 0)
            elif wall == 0:
                val = math.fabs(maze[i][j].f) * 5
                if val > 254:
                    val = 254
                pygame.draw.rect(screen, (val, 255, val), curRect, 0)
            if maze[i][j].payload == 2:
                screen.blit(itemIcon, (curRect[0], curRect[1]))


def getRandomEmptyBlock(maze):
    itemPos = Vector.Vector(random.randint(0, len(maze) - 1), random.randint(0, len(maze) - 1))
    while maze[itemPos.x][itemPos.y].wall == 1:
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
            maze[j][i].wall = int(fileRead[j])
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
    prettifyMaze(maze)
    return width / len(maze), N, maze, itemPos


def getSurrounding(maze, vec):
    xStart = vec.x
    yStart = vec.y
    n = len(maze)
    surroundingCount = 0

    x = xStart + 1
    y = yStart
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        surroundingCount += 1
    x = xStart
    y = yStart + 1
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        surroundingCount += 1
    x = xStart - 1
    y = yStart
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        surroundingCount += 1
    x = xStart
    y = yStart - 1
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        surroundingCount += 1
    return surroundingCount


def findNeighborWall(maze, vec):
    xStart = vec.x
    yStart = vec.y
    n = len(maze)

    x = xStart + 1
    y = yStart
    wallLocation = 0
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        wallLocation += 2
    x = xStart
    y = yStart + 1
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        wallLocation += 1
    x = xStart - 1
    y = yStart
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        wallLocation += 4
    x = xStart
    y = yStart - 1
    if 0 <= x < n and 0 <= y < n and maze[x][y].wall == 1:
        wallLocation += 8
    return wallLocation


def prettifyMaze(maze):
    outsideWallIcon = pygame.image.load('icons/wall.png')
    outsideWallIcon = pygame.transform.scale(outsideWallIcon, (TILE_SIZE, TILE_SIZE))
    normalInsideWallIcon = pygame.image.load('icons/normalInnerWall.png')
    normalInsideWallIcon = pygame.transform.scale(normalInsideWallIcon, (TILE_SIZE, TILE_SIZE))
    cornerInsideWallIcon = pygame.image.load('icons/cornerInnerWall.png')
    cornerInsideWallIcon = pygame.transform.scale(cornerInsideWallIcon, (TILE_SIZE, TILE_SIZE))
    floorIcon = pygame.image.load('icons/floor.png')
    floorIcon = pygame.transform.scale(floorIcon, (TILE_SIZE, TILE_SIZE))
    turnInnerWallIcon = pygame.image.load('icons/turnInnerWall.png')
    turnInnerWallIcon = pygame.transform.scale(turnInnerWallIcon, (TILE_SIZE, TILE_SIZE))
    TInnerWallIcon = pygame.image.load('icons/TInnerWall.png')
    TInnerWallIcon = pygame.transform.scale(TInnerWallIcon, (TILE_SIZE, TILE_SIZE))
    XInnerWallIcon = pygame.image.load('icons/XInnerWall.png')
    XInnerWallIcon = pygame.transform.scale(XInnerWallIcon, (TILE_SIZE, TILE_SIZE))

    for i in range(len(maze)):
        for j in range(len(maze)):
            nmbrOfSurroundingWalls = getSurrounding(maze, Vector.Vector(i, j))
            if i == 0 or j == 0 or i == len(maze) - 1 or j == len(maze) - 1 and maze[i][j].wall == 1:
                maze[i][j].setIcon(outsideWallIcon)
            elif maze[i][j].wall == 0:
                maze[i][j].setIcon(floorIcon)
            elif maze[i][j].wall == 1 and nmbrOfSurroundingWalls == 1:
                wallLocation = findNeighborWall(maze, Vector.Vector(i, j))
                angle = 0
                if wallLocation == 1:
                    angle = 180
                elif wallLocation == 2:
                    angle = 270
                elif wallLocation == 4:
                    angle = 90
                elif wallLocation == 8:
                    angle = 0
                else:
                    print "Problem finding a wall"
                maze[i][j].setIcon(pygame.transform.rotate(cornerInsideWallIcon, angle))
            elif maze[i][j].wall == 1 and nmbrOfSurroundingWalls == 2:
                # Here we are going to make the turn walls (e.i. 3, 6, 12, 9)
                wallLocation = findNeighborWall(maze, Vector.Vector(i, j))
                angle = 0
                icon = normalInsideWallIcon
                if wallLocation == 3:
                    angle = 0
                    icon = turnInnerWallIcon
                elif wallLocation == 5:
                    angle = 270
                    icon = turnInnerWallIcon
                elif wallLocation == 12:
                    angle = 180
                    icon = turnInnerWallIcon
                elif wallLocation == 10:
                    angle = 90
                    icon = turnInnerWallIcon
                # Here we are going to make the straight walls (e.i. 5 and 10)
                elif wallLocation == 6:
                    angle = 90
                    icon = normalInsideWallIcon
                elif wallLocation == 9:
                    angle = 0
                    icon = normalInsideWallIcon
                maze[i][j].setIcon(pygame.transform.rotate(icon, angle))

            elif maze[i][j].wall == 1 and nmbrOfSurroundingWalls == 3:
                wallLocation = findNeighborWall(maze, Vector.Vector(i, j))
                # Here we are going to make the T junctions (e.i. 7, 14, 13, 11)
                if wallLocation == 11:
                    angle = 90
                elif wallLocation == 7:
                    angle = 0
                elif wallLocation == 14:
                    angle = 180
                elif wallLocation == 13:
                    angle = 270
                maze[i][j].setIcon(pygame.transform.rotate(TInnerWallIcon, angle))
            elif maze[i][j].wall == 1 and nmbrOfSurroundingWalls == 4:
                maze[i][j].setIcon(XInnerWallIcon)


def GenerateMaze():
    maze = Generator.Maze(MAZE_SIZE, MAZE_SIZE)
    maze.generate()
    maze.toFile(maze.__str__())
    return readMaze()


def isWall(maze, x, y):
    if maze[x][y].wall != 1:
        return False
    return True


width = 800
height = 800
MAZE_SIZE = 10
TILE_SIZE = width / (MAZE_SIZE + 13)
print TILE_SIZE
GAME_SPEED = 350


def main():
    score = 0
    player = Player.Player(1, 15, (0, 0, 255), 'icons/player.png', TILE_SIZE)
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('ShopQuest')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    stepSize, N, maze, itemPos = GenerateMaze()
    ai = AI.AI(1, 3, (255, 0, 255), 'icons/AI.png', TILE_SIZE)

    bananaIcon = pygame.image.load('icons/banana.png')
    bananaIcon = pygame.transform.scale(bananaIcon, (TILE_SIZE, TILE_SIZE))

    showScreen(screen, maze, bananaIcon)
    player.drawCreature(screen, stepSize)
    pygame.display.update()
    clock = pygame.time.Clock()
    time = 0
    # Event loop
    while 1:
        showScreen(screen, maze, bananaIcon)
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
                    itemPos = getRandomEmptyBlock(maze)
                    maze[itemPos.x][itemPos.y].payload = 2
                    ai.path = []

        player.drawCreature(screen, stepSize)
        time += clock.get_time()
        if time > GAME_SPEED:
            time = 0
            # ai.moveInDirection(random.randint(0, 3), maze)
            ai.moveToNode(maze, maze[itemPos.x][itemPos.y])
            if ai.isOnItem(maze):
                maze[ai.pos.x][ai.pos.y].payload = 0
                itemPos = getRandomEmptyBlock(maze)
                maze[itemPos.x][itemPos.y].payload = 2
        ai.drawCreature(screen, stepSize)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__': main()
