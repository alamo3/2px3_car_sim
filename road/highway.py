import pygame.draw

from road.lane import Lane


def create_temp_straight_segment(lane, lane_width):
    mouse_pos = pygame.mouse.get_pos()
    end_point = translate_point_for_lane(mouse_pos, lane.lane_num, lane_width)
    lane.temp_segment_line(end_point)


def translate_point_for_lane(point, lane_num, lane_width):
    lane_origin_x = point[0] + (lane_width * lane_num)
    return lane_origin_x, point[1]


class Highway:

    def __init__(self, num_lanes, lane_width, origin_point):
        self.num_lanes = num_lanes
        self.lane_width = lane_width
        self.lanes = []
        self.editing_mode = False
        self.origin_point = None

        for i in range(num_lanes):
            self.lanes.append(Lane(i))

        self.set_origin(origin_point)

    def set_origin(self, point):

        for i in range(len(self.lanes)):
            lane = self.lanes[i]
            lane_origin = translate_point_for_lane(point, i, self.lane_width)
            lane.set_origin(lane_origin)

        self.origin_point = point

    def add_lane(self):
        self.num_lanes = self.num_lanes + 1

        new_lane = Lane(self.num_lanes - 1)
        new_lane_origin = translate_point_for_lane(self.origin_point, self.num_lanes-1, self.lane_width)

        new_lane.set_origin(new_lane_origin)

        self.lanes.append(new_lane)

    def draw_origin(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.origin_point, 10)

    def draw_lanes(self, surface):

        for i in range(self.num_lanes):
            if self.editing_mode:
                create_temp_straight_segment(self.lanes[i], self.lane_width)
            self.lanes[i].draw_lane(surface)

    def begin_adding_line_segment(self):
        self.editing_mode = True

    def complete_adding_line_segment(self):

        point = pygame.mouse.get_pos()
        for lane in self.lanes:
            lane_point = translate_point_for_lane(point, lane.lane_num, self.lane_width)
            lane.complete_temp_segment_line(lane_point)

        self.editing_mode = False
