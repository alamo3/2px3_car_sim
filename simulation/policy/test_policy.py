from simulation.policy.driving_policy import DrivingPolicy
import simulation.interface.highway_interface as hi
from car.car import Car
import car.car_manager as cm
import random


class TestPolicy(DrivingPolicy):

    def __init__(self):
        self.timer = 0

    def initialize(self):
        self.generate_car(0)

    def remove_completed_cars(self):
        cars_to_remove = [car for car in cm.cars if car.reached_end]
        cm.cars = [car for car in cm.cars if car not in cars_to_remove]

        for car in cars_to_remove:
            hi.highway.remove_car_from_lane(car)

    def generate_car(self, lane_num):
        car = Car(0.0, 0.0, 0.0, lane_num)
        hi.highway.add_car_to_lane(lane_num, car)
        cm.cars.append(car)

    def choose_new_lane(self, lane_num):
        if lane_num == 0:
            return 1
        elif lane_num == 1:
            return 2
        elif lane_num == 2:
            return 1

    def update(self, dt):
        self.timer = self.timer + dt
        self.remove_completed_cars()

        if len(cm.cars) == 0:
            self.generate_car(random.randint(0, 2))

        for car in cm.cars:
            car.move_forward_in_lane(dt)
            if self.timer > 5.0:
                car.perform_lane_change(self.choose_new_lane(car.lane_num))
                self.timer = 0.0



