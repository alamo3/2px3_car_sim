from road.road import  Road
import pygame
from pygame.locals import *

class StraightRoad (Road):

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.dir_vector = (p2[0] - p1[0], p2[1] - p1[1])

        Road.__init__(self, p1, p2)

    def draw(self, surface):
        pygame.draw.line(surface, (0,0,255), self.p1, self.p2)

