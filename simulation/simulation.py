import pygame
from pygame.locals import *

class Simulation:

    SIM_FPS = 30
    FPSTicker = pygame.time.Clock()

    def __init__(self):
        self.draw_surface = pygame.display.set_mode((1280, 720))
        self.draw_surface.fill((255,255,255))
        pygame.display.set_caption("Simulation Self-driving #26")

    def run(self):
        pass