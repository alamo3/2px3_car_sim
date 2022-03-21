import pygame
from pygame.locals import *

from ui.button_ident import ButtonIdent
from ui.window import Window
from ui.button import Button

from road.highway import Highway


class Simulation(Window):

    def __init__(self):
        Window.__init__(self, "Self-Driving #26 Highway Simulator")

        self.title = "HIGHWAY SIMULATOR"

        self.init_window()

        self.highway = Highway()

    def init_window(self):
        self.buttons.append(Button((10, 10), (90, 20), (255, 0, 0), "Load Highway", pygame.font.Font(None, 15),
                                   ButtonIdent.load_highway))

    def draw_highway(self):
        self.highway.draw_lanes(self.draw_surface)

    def run(self):
        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    super().quit()

            super().draw()

            self.draw_highway()

            super().run()
