import Vector
import pygame


class Creature:
    def __init__(self, x, y, color, filename):
        self.pos = Vector.Vector(x, y)
        self.color = color
        self.loadImage(filename)
        self.icon = self.loadImage(filename)

    def drawCreature(self, screen, stepSize):
        curRect = (self.pos.x * stepSize, self.pos.y * stepSize, stepSize - 2, stepSize - 2)
        # pygame.draw.rect(screen, self.color, curRect, 0)
        screen.blit(self.icon, (curRect[0], curRect[1]))

    def isOnItem(self, maze):
        x = self.pos.x
        y = self.pos.y
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload == 2:
            return True;
        return False;

    def loadImage(self, filename):
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, (15, 15))

    @staticmethod
    def checkEmpty(x, y, maze):
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload != 1:
            return True
        return False
