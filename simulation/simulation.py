import pygame
from pygame.locals import *

from ui.button_ident import ButtonIdent
from ui.window import Window
from ui.button import Button


class Simulation(Window):

    def __init__(self):
        Window.__init__(self, "Self-Driving #26 Highway Simulator")

        self.title = "HIGHWAY SIMULATOR"

        self.init_window()

    def init_window(self):
        self.buttons.append(Button((10, 10), (90, 20), (255, 0, 0), "Load Highway", pygame.font.Font(None, 15),
                                   ButtonIdent.load_highway))

    def run(self):
        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    super().quit()

            super().draw()

            super().run()
