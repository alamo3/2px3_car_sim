from abc import ABC
from abc import abstractmethod


class DrivingPolicy(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass
