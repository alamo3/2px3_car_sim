import math

import globalprops
from road.road import Road
from road.type import Type
import pygame
from geometry.Point import Point
from geometry.utils import Utils
from typing import List

BEZIER_RESOLUTION = 50


class Line:
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.dir_vector = Point(x1 - x, y1 - y)

    def get_length(self):
        return math.sqrt((self.x1 - self.x)**2 + (self.y1 - self.y)) * globalprops.KM_PER_UNIT

    def get_point_for_distance(self, distance):
        distance_sim = distance / globalprops.KM_PER_UNIT
        t = distance_sim / self.get_length()
        return Point(self.x + self.dir_vector.x * t, self.y + self.dir_vector.y * t)


class CurvedRoad(Road):

    def __init__(self, begin_point: Point, control_point: Point, end_point: Point):
        Road.__init__(self, begin_point, end_point, Type.curved)
        self.control_point = control_point
        self.segments: List[Line] = []

        self.calculate_curve()

    def calculate_point(self, t):
        x = (1 - t) * (1 - t) * self.start_p.x + 2 * (1 - t) * t * self.control_point.x + t * t * self.end_p.x
        y = (1 - t) * (1 - t) * self.start_p.y + 2 * (1 - t) * t * self.control_point.y + t * t * self.end_p.y

        return Point(x, y)

    def calculate_curve(self):
        self.segments = []
        prev_point = self.start_p

        for i in range(1, BEZIER_RESOLUTION):
            parameter = (1 / BEZIER_RESOLUTION) * i
            point = self.calculate_point(parameter)
            self.segments.append(Line(prev_point.x, prev_point.y, point.x, point.y))
            prev_point = point

    def points(self):
        return [self.start_p, self.control_point, self.end_p]

    def draw(self, surface):

        if globalprops.EDITING_MODE:
            self.calculate_curve()
            pygame.draw.circle(surface, (255, 0, 0), self.control_point.get_tuple(), 10)
            pygame.draw.circle(surface, (255, 0, 0), self.end_p.get_tuple(), 10)

        for line in self.segments:
            pygame.draw.line(surface, (0, 255, 0), (line.x, line.y), (line.x1, line.y1))

    def calculate_length(self):
        calculated_length = 0
        for line in self.segments:
            calculated_length = calculated_length + line.get_length()

        return calculated_length

    def calculate_parameter_distance(self, distance):
        pass

    def calculate_point_distance(self, distance):
        distance_accum = 0

        for segment in self.segments:
            distance_accum = distance_accum + segment.get_length()
            if distance_accum >= distance:
                remain_distance = distance_accum - distance
                return segment.get_point_for_distance(remain_distance)


    def export(self):
        return "CURVED,"+self.start_p.toString()+","+self.control_point.toString()+","+self.end_p.toString()
