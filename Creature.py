import Vector
import pygame


class Creature:
    """The base class for the interacting candidates"""
    def __init__(self, x, y, color, filename, tileSize):
        self.pos = Vector.Vector(x, y)
        self.color = color
        self.loadImage(filename, tileSize)
        self.icon = self.loadImage(filename, tileSize)

    def drawCreature(self, screen, stepSize):
        curRect = (self.pos.x * stepSize, self.pos.y * stepSize, stepSize - 2, stepSize - 2)
        screen.blit(self.icon, (curRect[0], curRect[1]))

    def isOnItem(self, maze):
        x = self.pos.x
        y = self.pos.y
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload == 2:
            return True;
        return False;

    def loadImage(self, filename, tileSize):
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, (tileSize, tileSize))

    @staticmethod
    def checkEmpty(x, y, maze):
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].wall != 1:
            return True
        return False
