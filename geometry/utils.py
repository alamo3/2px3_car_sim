from geometry.Point import Point
import math
from road.straight import StraightRoad
from road.curved import CurvedRoad


class Utils:

    @staticmethod
    def does_point_lie_in_circle(point: Point, circle_center: Point, circle_radius):
        sqx = (point.x - circle_center.x) ** 2
        sqy = (point.y - circle_center.y) ** 2

        return math.sqrt(sqx + sqy) < circle_radius

    @staticmethod
    def translate_point_horizontal(point: Point, dx):
        origin_x = point.x + dx
        return Point(origin_x, point.y)

    @staticmethod
    def translate_point_vertical(point: Point, dy):
        origin_y = point.y + dy
        return Point(point.x, origin_y)

    @staticmethod
    def translate_line_segment(segment: StraightRoad, dx):
        new_start = Utils.translate_point_horizontal(segment.start_p, dx)
        new_end = Utils.translate_point_horizontal(segment.end_p, dx)

        return StraightRoad(new_start, new_end)

    @staticmethod
    def translate_curved_segment(segment: CurvedRoad, dx):
        new_start = Utils.translate_point_horizontal(segment.start_p, dx)
        new_end = Utils.translate_point_horizontal(segment.end_p, dx)
        new_control = Utils.translate_point_horizontal(segment.control_point, dx)

        return CurvedRoad(new_start, new_control, new_end)
