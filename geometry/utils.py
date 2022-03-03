from geometry.Point import Point
import math


class Utils:

    @staticmethod
    def does_point_lie_in_circle(point: Point, circle_center: Point, circle_radius):
        sqx = (point.x - circle_center.x) ** 2
        sqy = (point.y - circle_center.y) ** 2

        return math.sqrt(sqx + sqy) < circle_radius
