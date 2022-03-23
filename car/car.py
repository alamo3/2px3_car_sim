import globalprops
import simulation.interface.highway_interface as highway_interface
from geometry.Point import Point
from road.road import Road

class Car:

    def __init__(self, reaction_time, risk_factor, following_distance, lane_num):
        self.reaction_time = reaction_time
        self.risk_factor = risk_factor
        self.following_distance = following_distance
        self.lane_num = lane_num
        self.speed = 0
        self.pos: Point = self.get_starting_pos()
        self.current_segment: Road = self.get_starting_segment()
        self.distance_on_segment = 0

    def get_starting_pos(self):
        lane = highway_interface.get_lane_by_id(self.lane_num)
        return lane.origin_point

    def get_starting_segment(self):
        lane = highway_interface.get_lane_by_id(self.lane_num)
        return lane.segments[0]


    def perform_lane_change(self):
        pass

    def adjust_following_distance(self):
        pass

    def adjust_reaction_time(self):
        pass

    def adjust_risk_factor(self):
        pass

    def move_forward_in_lane(self, delta_time):
        distance_travelled = delta_time * self.speed
        self.distance_on_segment = self.distance_on_segment + distance_travelled
        simulation_distance = distance_travelled / globalprops.KM_PER_UNIT

        parameter_segment = self.current_segment.calculate_parameter_distance(, )




