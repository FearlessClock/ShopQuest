from threading import Timer

import pygame


class Window:
    def __init__(self, windowSize, caption, TILE_SIZE):
        self.height = windowSize.y
        self.width = windowSize.x
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)

        self.bananaIcon = pygame.image.load('icons/banana.png')
        self.bananaIcon = pygame.transform.scale(self.bananaIcon, (TILE_SIZE, TILE_SIZE))

        self.explosionIcon = pygame.image.load('icons/explosion.png')
        self.explosionIcon = pygame.transform.scale(self.explosionIcon, (self.width/2, self.height/2))
        self.TILE_SIZE = TILE_SIZE
        self.popup = False

    def ShowPopUp(self):
        """The pop up shown is the item picked up pop up"""
        self.popup = True
        t = Timer(1.0, self.RemovePopUp)
        t.start()  # after 1 second, the pop up will be removed

    def RemovePopUp(self):
        self.popup = False

    def getSize(self):
        return self.screen.get_size()

    def clearScreen(self):
        background = pygame.Surface(self.getSize())
        background = background.convert()
        background.fill((250, 250, 250))

    def showScreen(self, maze, itemIcon):
        # Display the map
        stepSize = self.TILE_SIZE
        """For each cell, find the icon and show it on the screen"""
        for i in range(0, len(maze)):
            for j in range(0, len(maze[i])):
                curRect = (i * stepSize, j * stepSize, stepSize, stepSize)
                wall = maze[i][j].wall
                if wall == 1 or wall == 0:
                    if maze[i][j].icon is not None:
                        self.screen.blit(maze[i][j].icon, (curRect[0], curRect[1]))
                if maze[i][j].payload == 2:
                    self.screen.blit(itemIcon, (curRect[0], curRect[1]))

    def drawScreen(self, player, AI, maze):
        """Draw the screen, characters and pop up if activated"""
        self.showScreen(maze, self.bananaIcon)
        player.drawCreature(self.screen, self.TILE_SIZE)
        AI.drawCreature(self.screen, self.TILE_SIZE)
        if self.popup:
            self.ItemPickedUpPopUp()
        pygame.display.update()

    def ItemPickedUpPopUp(self):
        popUpRect = (self.height/4, self.width/4, 400, 180)
        self.screen.blit(self.explosionIcon, (popUpRect[0], popUpRect[1]))