from simulation.policy.driving_policy import DrivingPolicy
import simulation.interface.highway_interface as hi
from car.car import Car
import car.car_manager as cm
import random

car_id_generated = 0


class CarSpawner:
    def __init__(self, lane_num: int):
        self.lane_num = lane_num
        self.timer = 0
        self.next_car = self.get_next_car_time()

    def get_next_car_time(self):
        return random.uniform(10.0, 60.0)

    def generate_car(self, dt):
        global car_id_generated
        self.timer = self.timer + dt
        if self.timer > self.next_car:
            new_car = Car(0.0, 0.0, 0.0, self.lane_num, car_id_generated)
            hi.highway.add_car_to_lane(self.lane_num, new_car)
            cm.cars.append(new_car)
            car_id_generated = car_id_generated + 1
            self.next_car = self.get_next_car_time()
            self.timer = 0


class TestPolicy(DrivingPolicy):

    def __init__(self):
        self.timer = 0
        self.timer_second = 0
        self.generate_second = True
        self.first_lane = 0
        self.generators = [CarSpawner(0), CarSpawner(1), CarSpawner(2)]

    def initialize(self):
        pass

    def remove_completed_cars(self):
        cars_to_remove = [car for car in cm.cars if car.reached_end]
        cm.cars = [car for car in cm.cars if car not in cars_to_remove]

        for car in cars_to_remove:
            hi.highway.remove_car_from_lane(car)

    def choose_new_lane(self, lane_num):
        if lane_num == 0:
            return 1
        elif lane_num == 1:
            return 2
        elif lane_num == 2:
            return 1

    def update(self, dt):
        self.timer = self.timer + dt

        for gen in self.generators:
            gen.generate_car(dt)

        self.remove_completed_cars()

        for car in cm.cars:
            # if self.timer > 0.5:
            #     car.perform_lane_change(self.choose_new_lane(car.lane_num))
            #     self.timer = 0.0

            lead_car, dist = cm.get_lead_car(car)
            car.move_forward_in_lane(dt, lead_car, dist)


