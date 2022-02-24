import pygame.draw

from road.lane import Lane


class Highway:

    def __init__(self, num_lanes, lane_width, origin_point):
        self.num_lanes = num_lanes
        self.lane_width = lane_width
        self.lanes = []
        self.origin_point = origin_point

        for i in range(num_lanes):
            self.lanes.append(Lane(i))

    def add_lane(self):
        self.num_lanes = self.num_lanes + 1
        self.lanes.append(Lane(self.num_lanes - 1))

    def draw_origin(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.origin_point, 10)

    def draw_lanes(self, surface):

        for i in range(self.num_lanes):
            self.lanes[i].draw_lane()
