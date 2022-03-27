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
        return random.uniform(15.0, 20.0)

    def generate_car(self, dt):
        global car_id_generated
        self.timer = self.timer + dt
        if self.timer > self.next_car:
            num_cars = hi.get_num_cars_lane(self.lane_num)

            if num_cars > 40:
                self.reset_timers()
                return

            new_car = Car(0.0, self.lane_num, car_id_generated)

            reaction_time = self.generate_number(0.75, 2.0)
            min_follow = self.generate_number(150, 200)
            max_accel = self.generate_number(2.07, 5.5)
            comf_decel = self.generate_number(0.5, 1.0)
            max_speed = self.generate_number(130, 190)

            new_car.init_controller(min_follow, 2.1, reaction_time, max_accel, comf_decel, max_speed)

            hi.highway.add_car_to_lane(self.lane_num, new_car)
            cm.cars.append(new_car)
            car_id_generated = car_id_generated + 1

            self.reset_timers()

    def reset_timers(self):
        self.next_car = self.get_next_car_time()
        self.timer = 0

    def generate_number(self, low, high):
        return random.uniform(low, high)



class TestPolicy(DrivingPolicy):

    def __init__(self):
        self.timer = 0
        self.timer_second = 0
        self.generate_second = True
        self.first_lane = 0
        self.generators = [CarSpawner(0), CarSpawner(1), CarSpawner(2)]
        self.init_lane_properties()

    def init_lane_properties(self):
        hi.highway.lanes[0].speed_limit = 130
        hi.highway.lanes[1].speed_limit = 110
        hi.highway.lanes[2].speed_limit = 100

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


