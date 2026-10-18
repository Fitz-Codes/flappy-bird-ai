import pygame
import components

winHeight = 720
winWidth = 550
window = pygame.display.set_mode((winWidth, winHeight))

ground = components.Ground(winWidth)
pipes = []
