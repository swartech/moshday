

class Character:

    def __init__(self, x, y, img):
        import pygame
        from pygame.locals import *
        pygame.init()
        self.x = x
        self.y = y
        self.verticalSpeed = 0
        self.horizontalSpeed = 0
        self.img = pygame.image.load(img)
