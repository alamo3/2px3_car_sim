from road.road import Road
from road.type import Type
import pygame


class StraightRoad(Road):

    def __init__(self, p1, p2):

        Road.__init__(self, p1, p2, Type.straight)
        self.dir_vector = None

        if p2 is not None:
            self.dir_vector = (p2[0] - p1[0], p2[1] - p1[1])

    def draw(self, surface):

        if (self.start_p is not None) and (self.end_p is not None):
            pygame.draw.line(surface, (0, 0, 255), self.start_p, self.end_p)


