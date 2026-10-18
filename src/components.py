import pygame
import random

class Ground:
    groundLevel = 500

    def __init__(self , winWidth):
        self.x, self.y = 0, Ground.groundLevel
        self.rect = pygame.Rect(self.x, self.y, winWidth, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipe:
    width = 15
    opening = 100

    def __init__(self, winWidth):
        self.x = winWidth
        self.bottomHeight = random.randint(10, 100)
        self.topHeight = Ground.groundLevel - self.bottomHeight - self.opening
        self.bottomRect, self.topRect = pygame.Rect(0, 0, 0, 0,), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.offScreen = False

    def draw(self, window):
        self.bottomRect = pygame.Rect(self.x, Ground.groundLevel - self.bottomHeight, self.width, self.bottomHeight)
        pygame.draw.rect(window, (255, 255, 255), self.bottomRect)

        self.topRect = pygame.Rect(self.x, 0, self.width, self.topHeight)
        pygame.draw.rect(window, (255, 255, 255), self.topRect)

    def update(self):
        self.x -= 1
        if self.x + Pipe.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.offScreen = True