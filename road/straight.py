import globalprops
from road.road import Road
from road.type import Type
import pygame
from geometry.Point import Point


class StraightRoad(Road):

    def __init__(self, p1: Point, p2: Point):

        Road.__init__(self, p1, p2, Type.straight)
        self.dir_vector = None

        if p2 is not None:
            self.dir_vector = (p2.x - p1.x, p2.y - p1.y)

    def draw(self, surface):

        if globalprops.EDITING_MODE:
            #pygame.draw.circle(surface, (255, 0, 0), self.start_p, 10)
            pygame.draw.circle(surface, (255, 0, 0), self.end_p.get_tuple(), 10)

        if (self.start_p is not None) and (self.end_p is not None):
            pygame.draw.line(surface, (0, 0, 255), self.start_p.get_tuple(), self.end_p.get_tuple())


