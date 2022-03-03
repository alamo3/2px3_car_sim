import pygame.draw

from road.lane import Lane
from geometry.Point import Point
from geometry.utils import Utils


def create_temp_straight_segment(lane, lane_width):
    mouse_pos = pygame.mouse.get_pos()
    end_point = translate_point_for_lane(Point.t2p(mouse_pos), lane.lane_num, lane_width)
    lane.temp_segment_line(end_point)


def create_temp_curved_segment(lane, lane_width, end_point: Point):
    mouse_pos = pygame.mouse.get_pos()
    end_point_lane = translate_point_for_lane(end_point, lane.lane_num, lane_width)
    control_point_lane = translate_point_for_lane(Point.t2p(mouse_pos), lane.lane_num, lane_width)
    lane.temp_segment_curve(end_point_lane, control_point_lane)


def translate_point_for_lane(point: Point, lane_num, lane_width):
    lane_origin_x = point.x + (lane_width * lane_num)
    return Point(lane_origin_x, point.y)


class Highway:

    def __init__(self, num_lanes, lane_width, origin_point):
        self.num_lanes = num_lanes
        self.lane_width = lane_width
        self.lanes = []
        self.entry_ramps = []
        self.exit_ramps = []

        self.editing_mode = False
        self.origin_point = None

        self.editing_mode_curve = False
        self.temp_curve_end_point = None

        self.editing_segment = False

        for i in range(num_lanes):
            self.lanes.append(Lane(i))

        self.set_origin(origin_point)

    def set_origin(self, point):

        for i in range(len(self.lanes)):
            lane = self.lanes[i]
            lane_origin = translate_point_for_lane(Point.t2p(point), i, self.lane_width)
            lane.set_origin(lane_origin)

        self.origin_point = Point.t2p(point)

    def add_lane(self):
        self.num_lanes = self.num_lanes + 1

        prev_lane = self.lanes[-1]

        new_lane = prev_lane.create_translated_copy(self.lane_width, self.num_lanes - 1)

        self.lanes.append(new_lane)

    def draw_origin(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.origin_point, 10)

    def draw_lanes(self, surface):

        if self.editing_mode_curve and self.temp_curve_end_point is not None:
            pygame.draw.circle(surface, (0, 0, 0), self.temp_curve_end_point, 10)
        elif self.editing_mode:
            pygame.draw.circle(surface, (0, 0, 0), pygame.mouse.get_pos(), 10)

        for i in range(self.num_lanes):
            if self.editing_mode:
                create_temp_straight_segment(self.lanes[i], self.lane_width)
            elif self.editing_mode_curve and self.temp_curve_end_point is not None:
                create_temp_curved_segment(self.lanes[i], self.lane_width, Point.t2p(self.temp_curve_end_point))
            self.lanes[i].draw_lane(surface)

    def begin_adding_line_segment(self):
        self.editing_mode = True

    def begin_adding_curve_segment(self):
        self.editing_mode_curve = True

    def select_curve_endpoint(self, point):
        self.temp_curve_end_point = point

    def complete_adding_curve_segment(self, point):
        for lane in self.lanes:
            end_point = translate_point_for_lane(Point.t2p(self.temp_curve_end_point), lane.lane_num, self.lane_width)
            control_point = translate_point_for_lane(Point.t2p(point), lane.lane_num, self.lane_width)
            lane.complete_temp_segment_curve(end_point, control_point)

        self.editing_mode_curve = False
        self.temp_curve_end_point = None

    def complete_adding_line_segment(self):

        point = pygame.mouse.get_pos()
        for lane in self.lanes:
            lane_point = translate_point_for_lane(Point.t2p(point), lane.lane_num, self.lane_width)
            lane.complete_temp_segment_line(lane_point)

        self.editing_mode = False

    def does_highway_have_segments(self):
        for lane in self.lanes:
            if len(lane.segments) != 0:
                return True

        return False

    def begin_editing_segments(self):
        self.editing_segment = True

    def get_lane_by_mouse_click(self):

        point = pygame.mouse.get_pos()
        p0 = Point.t2p(point)

        for lane in self.lanes:
            origin_lane = lane.origin_point
            if Utils.does_point_lie_in_circle(p0, origin_lane, 10):
                return lane

    def does_mouse_click_intersect_point(self):

        point = pygame.mouse.get_pos()

        for lane in self.lanes:
            p1 = lane.does_point_intersect_control_points(Point.t2p(point))
            if p1 is not None:
                p1.x = point[0]
                p1.y = point[1]
                return True

        return False
