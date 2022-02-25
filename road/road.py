from abc import ABC, abstractmethod


class Road(ABC):

    def __init__(self, start_p, end_p):
        self.start_p = start_p
        self.end_p = end_p

    @abstractmethod
    def draw(self, surface):
        pass
