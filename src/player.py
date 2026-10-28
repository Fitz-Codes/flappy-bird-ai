import pygame
import random
import config
import brain

class Player:
    def __init__(self):
        #Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        #AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

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
            if self.vel > 5:
                self.vel = 5
            #Increment lifespan
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p
        return None

    #AI functions
    def look(self): #Calculates players vision, followed by drawing a line to represent that distance
        pipe = self.closest_pipe()
        if pipe is None:
            self.vision = [0.5, 1, 0.5]
            return

        # Vertical distance to the bottom of the top pipe.
        self.vision[0] = max(0, self.rect.center[1] - pipe.topRect.bottom) / 500
        pygame.draw.line(config.window, self.color, self.rect.center,
                         (self.rect.center[0], pipe.topRect.bottom))

        # Vertical distance to the top of the bottom pipe.
        self.vision[1] = max(0, pipe.bottomRect.top - self.rect.center[1]) / 500
        pygame.draw.line(config.window, self.color, self.rect.center,
                         (self.rect.center[0], pipe.bottomRect.top))

        # Horizontal distance to the middle of the upcoming pair of pipes.
        self.vision[2] = max(0, pipe.x - self.rect.center[0]) / 500
        pygame.draw.line(config.window, self.color, self.rect.center,
                         (pipe.x, self.rect.center[1]))
    
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > .73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone