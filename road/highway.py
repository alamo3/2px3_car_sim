from road.lane import Lane


class Highway:

    def __init__(self, num_lanes, lane_width):
        self.num_lanes = num_lanes
        self.lane_width = lane_width
        self.lanes = []

        for i in range(num_lanes):
            self.lanes.append(Lane(i))

    def draw_lanes(self, surface):

        for i in range(self.num_lanes):
            self.lanes[i].draw_lane()
