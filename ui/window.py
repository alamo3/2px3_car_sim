import pygame
from abc import ABC
from abc import abstractmethod


# static function to get if left mouse button is pressed
def get_mouse_clicked():
    return pygame.mouse.get_pressed()[0]


class Window(ABC):
    SIM_FPS = 30  # simulator runs at 30 fps
    FPSTicker = pygame.time.Clock()  # create pygame fps clock

    def __init__(self, window_title):

        # set up pygame window rendering
        pygame.init()
        self.draw_surface = pygame.display.set_mode((1920, 900))
        self.draw_surface.fill((255, 255, 255))

        self.title = window_title

        pygame.display.set_caption(window_title)

        # buttons
        self.buttons = []

    @abstractmethod
    def init_window(self):
        pass

    def draw_buttons(self):

        # draw buttons if they are visible. appropriate co-ordinates set by states
        for button in self.buttons:
            if button.is_visible:
                button.draw(self.draw_surface)

    def draw_title(self):
        txt_surface = pygame.font.Font(None, 25).render(self.title, True, (0, 0, 0))
        self.draw_surface.blit(txt_surface, (640, 10))

    def quit(self):
        pygame.quit()
        exit(0)

    def draw(self):
        self.draw_surface.fill((255, 255, 255))
        self.draw_title()
        self.draw_buttons()

    def run(self):
        pygame.display.update()  # update the display and delay if necessary for locked FPS
        self.FPSTicker.tick(self.SIM_FPS)
