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

    #
    # def x(self):
    #     return self.x
    #
    # def y(self):
    #     return self.Y

    def posArray(self):
        return [self.x, self.y]


class Creature:
    def __init__(self, x, y, color):
        self.pos = Vector(x, y)
        self.color = color

    def drawCreature(self, screen, stepSize):
        curRect = (self.pos.x * stepSize + 2, self.pos.y * stepSize + 2, stepSize - 2, stepSize - 2)
        pygame.draw.rect(screen, self.color, curRect, 0)

    def isOnItem(self, maze):
        if maze[self.pos.x][self.pos.y] == 2:
            return True;
        return False;


class Player(Creature):
    def __init__(self, x, y, color):
        Creature.__init__(x, y, color)

        self.up = 273
        self.down = 274
        self.right = 275
        self.left = 276

        self.speed = 1

    def move(self, key, maze):
        if key == self.up and maze[self.pos.x][self.pos.y - 1] != 1:
            self.pos.y -= self.speed
        elif key == self.down and maze[self.pos.x][self.pos.y + 1] != 1:
            self.pos.y += self.speed
        elif key == self.left and maze[self.pos.x - 1][self.pos.y] != 1:
            self.pos.x -= self.speed
        elif key == self.right and maze[self.pos.x + 1][self.pos.y] != 1:
            self.pos.x += self.speed


class AI(Creature):
    def __init__(self, x, y, color):
        Creature.__init__(x, y, color)
        self.pos = Vector(x, y)

    def moveInDirection(self, direction, maze):
        if direction == 0:
            if self.pos.x > 0:
                self.pos.x -= 1
        elif direction == 1:
            if self.pos.y > 0:
                self.pos.y -= 1
        elif direction == 2:
            if self.pos.x < len(maze):
                self.pos.x += 1
        elif direction == 3:
            if self.pos.y < len(maze):
                self.pos.y += 1

def showScreen(screen, maze):
    # Display the map
    stepSize = width / len(maze)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            curRect = (i * stepSize + 1, j * stepSize + 1, stepSize - 1, stepSize - 1)
            if maze[i][j] == 1:
                pygame.draw.rect(screen, (255, 0, 0), curRect, 0)
            elif maze[i][j] == 0:
                pygame.draw.rect(screen, (0, 255, 0), curRect, 0)
            elif maze[i][j] == 2:
                pygame.draw.rect(screen, (255, 100, 0), curRect, 0)


def readMaze():
    # Read the file containing the maze
    f = open('maze.txt', 'r')
    N = int(f.readline())
    maze = []
    for i in range(N):
        maze.append([])
        for j in range(N):
            maze[i].append(0)
    for i in range(N):
        fileRead = f.readline().split()
        for j in range(len(fileRead)):
            maze[j][i] = int(fileRead[j])
    f.close()
    return width / len(maze), N, maze


width = 400
height = 400


def main():
    score = 0
    player = Player(1, 15)
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    stepSize, N, maze = readMaze()
    ai = AI(2, 3, N)
    showScreen(screen, maze)
    player.drawPlayer(screen, stepSize)
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
                    maze[player.pos.x][player.pos.y] = 0
                    score += 1
                    print score
                    maze[random.randint(0, N - 1)][random.randint(0, N - 1)] = 2
                showScreen(screen, maze)
                player.drawPlayer(screen, stepSize)
                ai.moveInDirection(random.randint(0, 3))
                ai.drawAI(screen, stepSize)
                pygame.display.update()


if __name__ == '__main__': main()
