from car.car import Car

SD_FOLLOW_DISTANCE = 2.0
SD_REACTION_TIME = 0.004


class SDCar(Car):

    def __init__(self, lane_num):
        Car.__init__(self, SD_REACTION_TIME, 0, SD_FOLLOW_DISTANCE, lane_num)
        



