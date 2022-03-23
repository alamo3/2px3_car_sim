import simulation.interface.highway_interface as highway_interface
import simulation.interface.sim_interface as sim_interface

from abc import ABC
from abc import abstractmethod


class DrivingPolicy(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self):
        pass
