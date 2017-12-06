from threading import Timer

import pygame


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


class Window():
    def __init__(self, windowSize, caption, TILE_SIZE):
        self.height = windowSize.x
        self.width = windowSize.y
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)

        self.bananaIcon = pygame.image.load('icons/banana.png')
        self.bananaIcon = pygame.transform.scale(self.bananaIcon, (TILE_SIZE, TILE_SIZE))

        self.explosionIcon = pygame.image.load('icons/explosion.png')
        self.explosionIcon = pygame.transform.scale(self.explosionIcon, (700, 300))
        self.TILE_SIZE = TILE_SIZE
        self.popup = False

    def ShowPopUp(self):
        self.popup = True
        t = Timer(1.0, self.RemovePopUp)
        t.start()  # after 30 seconds, "hello, world" will be printed

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
        for i in range(0, len(maze)):
            for j in range(0, len(maze[i])):
                curRect = (i * stepSize, j * stepSize, stepSize, stepSize)
                wall = maze[i][j].wall
                if wall == 1 or wall == 0:
                    if maze[i][j].icon is not None:
                        self.screen.blit(maze[i][j].icon, (curRect[0], curRect[1]))
                        # pygame.draw.rect(screen, (255, 0, 0), curRect, 0)
                elif wall == 0:
                    val = pygame.math.fabs(maze[i][j].f) * 5
                    if val > 254:
                        val = 254
                    pygame.draw.rect(self.screen, (val, 255, val), curRect, 0)
                if maze[i][j].payload == 2:
                    self.screen.blit(itemIcon, (curRect[0], curRect[1]))

    def drawScreen(self, player, AI, maze):
        self.showScreen(maze, self.bananaIcon)
        player.drawCreature(self.screen, self.TILE_SIZE)
        AI.drawCreature(self.screen, self.TILE_SIZE)
        if self.popup:
            self.ItemPickedUpPopUp()
        pygame.display.update()

    def ItemPickedUpPopUp(self):
        popUpRect = (100, 300, 400, 180)
        self.screen.blit(self.explosionIcon, (popUpRect[0], popUpRect[1]))

        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Item picked up!!", largeText)
        TextRect.center = (popUpRect[0]+700/2, popUpRect[1]+popUpRect[1]/2)
        self.screen.blit(TextSurf, TextRect)