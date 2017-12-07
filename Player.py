import Creature


class Player(Creature.Creature):
    """Structure to store the player information"""
    def __init__(self, x, y, color, filename, tileSize):
        Creature.Creature.__init__(self, x, y, color, filename, tileSize)
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
