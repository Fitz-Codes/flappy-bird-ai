import pygame
import random
import config

class Player:
    def __init__(self):
        #Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        #AI
        self.decision = None

    #Game related functions
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 30)

    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.topRect) or \
                   pygame.Rect.colliderect(self.rect, p.bottomRect)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            #Gravity
            self.vel += 0.25
            self.rect.y += self.vel