from abc import ABC, abstractmethod
from road.type import Type


class Road(ABC):

    def __init__(self, start_p, end_p, type: Type):
        self.start_p = start_p
        self.end_p = end_p
        self.road_type = type

    @abstractmethod
    def draw(self, surface):
        pass
