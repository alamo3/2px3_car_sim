import tkinter.messagebox

import pygame
from pygame.locals import *

from ui.button_ident import ButtonIdent
from ui.window import Window
from ui.button import Button

from road.highway import Highway

from tkinter import filedialog as fd


class Simulation(Window):

    def __init__(self):
        Window.__init__(self, "Self-Driving #26 Highway Simulator")

        self.title = "HIGHWAY SIMULATOR"

        self.init_window()

        self.highway = None

    def init_window(self):
        self.buttons.append(Button((10, 10), (90, 20), (255, 0, 0), "Load Highway", pygame.font.Font(None, 15),
                                   ButtonIdent.load_highway))

    def draw_highway(self):
        if self.highway is not None:
            self.highway.draw_lanes(self.draw_surface)

    def load_highway(self):
        try:
            file_name = fd.askopenfilename()
            self.highway = Highway()
            self.highway.load_highway(file_name)
        except:
            tkinter.messagebox.showerror(title='Road Simulator', message='Error loading highway from file!')
            self.highway = None

    def run(self):
        while True:

            for event in pygame.event.get():

                for button in self.buttons:
                    if button.clicked(event) and event.type == MOUSEBUTTONUP:
                        self.load_highway()

                if event.type == pygame.QUIT:
                    super().quit()

            super().draw()

            self.draw_highway()

            super().run()
