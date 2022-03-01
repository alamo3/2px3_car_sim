import geometry

from road.straight import StraightRoad
from road.curved import CurvedRoad
from road.type import Type
import pygame
from geometry.Point import Point
from road.road import Road
import math


def translate_point_horizontal(point: Point, dx):
    lane_origin_x = point.x + dx
    return Point(lane_origin_x, point.y)


def translate_line_segment(segment: StraightRoad, dx):
    new_start = translate_point_horizontal(segment.start_p, dx)
    new_end = translate_point_horizontal(segment.end_p, dx)

    return StraightRoad(new_start, new_end)


def translate_curved_segment(segment: CurvedRoad, dx):
    new_start = translate_point_horizontal(segment.start_p, dx)
    new_end = translate_point_horizontal(segment.end_p, dx)
    new_control = translate_point_horizontal(segment.control_point, dx)

    return CurvedRoad(new_start, new_control, new_end)


class Lane:

    def __init__(self, lane_num):
        self.segments = []
        self.lane_num = lane_num
        self.origin_point: Point = None
        self.lane_txt = pygame.font.Font(None, 15).render("Lane " + str(self.lane_num), True, (0, 0, 0))
        self.temp_segment = None

    def set_origin(self, point: Point):
        self.origin_point = point

    def create_new_straight_road(self, end_point: Point):

        if len(self.segments) == 0:
            return StraightRoad(self.origin_point, end_point)
        else:
            final_point = self.segments[-1].end_p
            return StraightRoad(final_point, end_point)

    def create_new_curved_road(self, end_point: Point, control_point: Point):
        if len(self.segments) == 0:
            return CurvedRoad(self.origin_point, control_point, end_point)
        else:
            final_point = self.segments[-1].end_p
            return CurvedRoad(final_point, control_point, end_point)

    def temp_segment_curve(self, end_point: Point, control_point: Point):
        self.temp_segment = self.create_new_curved_road(end_point, control_point)

    def complete_temp_segment_curve(self, end_point: Point, control_point: Point):
        new_segment = self.create_new_curved_road(end_point, control_point)
        self.segments.append(new_segment)
        self.temp_segment = None

    def temp_segment_line(self, end_point: Point):
        self.temp_segment = self.create_new_straight_road(end_point)

    def complete_temp_segment_line(self, end_point: Point):
        new_segment = self.create_new_straight_road(end_point)
        self.segments.append(new_segment)
        self.temp_segment = None

    def get_last_segment(self):
        if not len(self.segments) == 0:
            return self.segments[-1]

    def create_translated_copy(self, dx, lane_num):
        lane = Lane(lane_num)

        new_segments = []
        for segment in self.segments:
            if segment.road_type == Type.straight:
                new_segment = translate_line_segment(segment, dx)

            else:
                new_segment = translate_curved_segment(segment, dx)

            if not len(new_segments) == 0:
                last_segment = new_segments[-1]
                new_segment.start_p = last_segment.end_p

            new_segments.append(new_segment)

        lane.origin_point = translate_point_horizontal(self.origin_point, dx)
        lane.segments = new_segments

        return lane

    def does_point_intersect_control_points(self, p0: Point):

        if len(self.segments) == 0:
            return False

        for segment in self.segments:
            for p1 in segment.points():
                sqx = (p0.x - p1.x) ** 2
                sqy = (p0.y - p1.y) ** 2

                if math.sqrt(sqx + sqy) < 10:
                    print("Intersected point")
                    return p1

    def draw_lane(self, surface):

        if self.origin_point is not None:
            pygame.draw.circle(surface, (0, 0, 0), self.origin_point.get_tuple(), 10.0)
            surface.blit(self.lane_txt, (self.origin_point.x - 10, self.origin_point.y + 12))

        for segment in self.segments:
            segment.draw(surface)

        if self.temp_segment is not None:
            self.temp_segment.draw(surface)
