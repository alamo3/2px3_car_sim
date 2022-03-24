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
        self.speed = 70
        self.pos: Point = self.get_starting_pos()
        self.segment_num = 0
        self.current_segment: Road = self.get_segment()
        self.distance_on_segment = 0
        self.reached_end = False
        self.distance_total = 0
        self.debug_changed_lane = False

    def get_starting_pos(self):
        lane = self.get_lane()
        return lane.origin_point

    def get_segment(self):
        lane = self.get_lane()
        return lane.segments[self.segment_num]

    def perform_lane_change(self, new_lane_num):
        new_lane = highway_interface.get_lane_by_id(new_lane_num)
        prev_lane = self.get_lane()
        new_segment_pos = new_lane.get_position_on_lane(self.get_segment(), self.pos)

        if new_segment_pos[0] is None:
            return  # abort lane change, not possible

        self.pos = new_segment_pos[0]
        self.lane_num = new_lane_num
        self.segment_num = new_segment_pos[1]
        self.distance_on_segment = new_segment_pos[2]
        self.current_segment = self.get_segment()
        self.debug_changed_lane = True
        prev_lane.cars.remove(self)
        new_lane.cars.append(self)



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

        if self.debug_changed_lane:
            print("Break")
            self.debug_changed_lane = False

        distance_travelled = delta_time * self.speed
        self.distance_on_segment = self.distance_on_segment + distance_travelled
        self.distance_total = self.distance_total + distance_travelled

        if self.distance_on_segment > self.current_segment.calculate_length():
            remaining_distance = self.distance_on_segment - self.current_segment.calculate_length()

            if self.segment_num == (len(self.get_lane().segments) - 1):
                self.reached_end = True
                return

            self.get_next_segment()
            self.distance_on_segment = remaining_distance
            self.pos = self.current_segment.calculate_point_distance(self.distance_on_segment)
        else:
            self.pos = self.current_segment.calculate_point_distance(self.distance_on_segment)

    def draw(self, draw_surface):
        pygame.draw.circle(draw_surface, (206, 0, 252), self.pos.get_tuple(), 10)
