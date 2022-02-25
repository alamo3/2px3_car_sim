import pygame
from pygame.locals import *
from ui.button import Button
from enum import Enum
from road.highway import Highway


class DesignerState(Enum):
    none = 0,
    choosing_origin = 1,
    creatingStraightLine = 2


def get_mouse_clicked():
    return pygame.mouse.get_pressed()[0]


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
        self.choose_origin = None
        self.remove_lane = None
        self.add_straight_segment = None
        self.state = DesignerState.none

        self.init_menu()

        self.highway = Highway(1, 70, (450, 680))

    def init_menu(self):
        self.add_lane = Button((10, 10), (70, 20), (255, 0, 0), "Add Lane", pygame.font.Font(None, 15))
        self.remove_lane = Button((10, 40), (90, 20), (255, 0, 0), "Remove Lane", pygame.font.Font(None, 15))
        self.choose_origin = Button((10, 70), (120, 20), (255, 0, 0), "Choose Origin Point", pygame.font.Font(None, 15))
        self.add_straight_segment = Button((10, 100), (120, 20), (255, 0, 0), "Add Straight Segment", pygame.font.Font(None, 15))

    def draw_buttons(self):
        self.add_lane.draw(self.draw_surface)
        self.choose_origin.draw(self.draw_surface)
        self.remove_lane.draw(self.draw_surface)
        self.add_straight_segment.draw(self.draw_surface)

    def draw_title(self, text):
        txt_surface = pygame.font.Font(None, 25).render(text, True, (0, 0, 0))
        self.draw_surface.blit(txt_surface, (640, 10))

    def draw_highway(self):
        #self.highway.draw_origin(self.draw_surface)
        self.highway.draw_lanes(self.draw_surface)

    def choose_origin_point(self):
        self.draw_title("choose origin point for highway")

        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.draw_surface, (0, 0, 0), mouse_pos, 10)

        mouse_click = pygame.mouse.get_pressed()[0]

        if get_mouse_clicked():
            self.highway.set_origin(mouse_pos)
            self.state = DesignerState.none

    def adding_line_segment(self):
        self.draw_title("Add line segment to highway")

        if get_mouse_clicked():
            self.highway.complete_adding_line_segment()
            self.state = DesignerState.none


    def run(self):
        run_designer = True
        while run_designer:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.add_lane.clicked(event):
                        self.highway.add_lane()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.choose_origin.clicked(event):
                        self.state = DesignerState.choosing_origin

                    if self.add_straight_segment.clicked(event):
                        self.state = DesignerState.creatingStraightLine
                        self.highway.begin_adding_line_segment()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            self.draw_surface.fill((255, 255, 255))
            self.draw_buttons()
            self.draw_highway()

            match self.state:
                case DesignerState.none:
                    pass
                case DesignerState.choosing_origin:
                    self.choose_origin_point()
                case DesignerState.creatingStraightLine:
                    self.adding_line_segment()

            pygame.display.update()
            Designer.FPSTicker.tick(Designer.SIM_FPS)
