import globalprops
import simulation.interface.highway_interface as highway_interface
from geometry.Point import Point
from road.road import Road
import pygame

class Car:

    def __init__(self, reaction_time, risk_factor, following_distance, lane_num):
        self.reaction_time = reaction_time
        self.risk_factor = risk_factor
        self.following_distance = following_distance
        self.lane_num = lane_num
        self.speed = 0
        self.pos: Point = self.get_starting_pos()
        self.current_segment: Road = self.get_segment()
        self.distance_on_segment = 0
        self.segment_num = 0

    def get_starting_pos(self):
        lane = self.get_lane()
        return lane.origin_point

    def get_segment(self):
        lane = self.get_lane()
        return lane.segments[self.segment_num]

    def perform_lane_change(self):
        pass

    def adjust_following_distance(self):
        pass

    def adjust_reaction_time(self):
        pass

    def adjust_risk_factor(self):
        pass

    def get_next_segment(self):
        self.segment_num = self.segment_num + 1
        self.current_segment = self.get_segment()

    def get_lane(self):
        return highway_interface.get_lane_by_id(self.lane_num)

    def move_forward_in_lane(self, delta_time):
        distance_travelled = delta_time * self.speed
        self.distance_on_segment = self.distance_on_segment + distance_travelled

        if self.distance_on_segment > self.current_segment.calculate_length():
            remaining_distance = self.distance_on_segment - self.current_segment.calculate_length()
            self.get_next_segment()
            self.distance_on_segment = remaining_distance
            self.pos = self.current_segment.calculate_point_distance(self.distance_on_segment)

        else:
            self.pos = self.current_segment.calculate_point_distance(self.distance_on_segment)

    def draw(self, draw_surface):
        pygame.draw.circle(draw_surface, (206, 0, 252), self.pos.get_tuple(), 10)




