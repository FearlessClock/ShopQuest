import Vector
import pygame



class Creature:
    def __init__(self, x, y, color):
        self.pos = Vector.Vector(x, y)
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
