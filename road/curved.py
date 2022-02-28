import globalprops
from road.road import Road
from road.type import Type
import pygame

BEZIER_RESOLUTION = 50


class Line:
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1


class CurvedRoad(Road):

    def __init__(self, begin_point, control_point, end_point):
        Road.__init__(self, begin_point, end_point, Type.curved)
        self.control_point = control_point
        self.segments = []

        self.calculate_curve()

    def calculate_point(self, t):
        x = (1 - t) * (1 - t) * self.start_p[0] + 2 * (1 - t) * t * self.control_point[0] + t * t * self.end_p[0]
        y = (1 - t) * (1 - t) * self.start_p[1] + 2 * (1 - t) * t * self.control_point[1] + t * t * self.end_p[1]

        return x, y

    def calculate_curve(self):
        prev_point = self.start_p

        for i in range(1, BEZIER_RESOLUTION):
            parameter = (1 / BEZIER_RESOLUTION) * i
            point = self.calculate_point(parameter)
            self.segments.append(Line(prev_point[0], prev_point[1], point[0], point[1]))
            prev_point = point

    def points(self):
        return [self.start_p, self.control_point, self.end_p]

    def draw(self, surface):

        if globalprops.EDITING_MODE:
            #pygame.draw.circle(surface, (255, 0, 0), self.start_p, 10)
            pygame.draw.circle(surface, (255, 0, 0), self.control_point, 10)
            pygame.draw.circle(surface, (255, 0, 0), self.end_p, 10)

        for line in self.segments:
            pygame.draw.line(surface, (0, 255, 0), (line.x, line.y), (line.x1, line.y1))
