import pygame
from pygame.locals import *
from ui.button import Button


class Designer:
    SIM_FPS = 30
    FPSTicker = pygame.time.Clock()

    def __init__(self):

        pygame.init()
        self.draw_surface = pygame.display.set_mode((1280, 720))
        self.draw_surface.fill((255, 255, 255))
        pygame.display.set_caption("Road Designer Self-driving #26")

        # buttons
        self.add_lane = None

        self.init_menu()

    def init_menu(self):
        self.add_lane = Button((10, 10), (70, 20), (255, 0, 0), "Add Lane", pygame.font.Font(None, 15))

    def run(self):
        run_designer = True
        while run_designer:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.add_lane.clicked(event):
                        print("Clicked")

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            self.draw_surface.fill((255,255,255))
            self.add_lane.draw(self.draw_surface)

            pygame.display.update()
            Designer.FPSTicker.tick(Designer.SIM_FPS)
