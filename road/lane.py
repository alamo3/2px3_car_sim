from road.straight import StraightRoad
import pygame
from pygame.locals import *


class Lane:

    def __init__(self, lane_num):
        self.segments = []
        self.lane_num = lane_num
        self.origin_point = None
        self.lane_txt = pygame.font.Font(None, 15).render("Lane " + str(self.lane_num), True, (0, 0, 0))
        self.temp_segment = None

    def set_origin(self, point):
        self.origin_point = point

    def create_new_straight_road(self, end_point):

        if len(self.segments) == 0:
            return StraightRoad(self.origin_point, end_point)
        else:
            final_point = self.segments[-1].end_p
            return StraightRoad(final_point, end_point)

    def temp_segment_line(self, end_point):
        self.temp_segment = self.create_new_straight_road(end_point)

    def complete_temp_segment_line(self, end_point):
        new_segment = self.create_new_straight_road(end_point)
        self.segments.append(new_segment)
        self.temp_segment = None

    def draw_lane(self, surface):

        if self.origin_point is not None:
            pygame.draw.circle(surface, (0, 0, 0), self.origin_point, 10.0)
            surface.blit(self.lane_txt, (self.origin_point[0]-10, self.origin_point[1] + 12))

        for segment in self.segments:
            segment.draw(surface)

        if self.temp_segment is not None:
            self.temp_segment.draw(surface)
