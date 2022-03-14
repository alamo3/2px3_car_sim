import pygame

from ui.button_ident import ButtonIdent
from ui.button import Button

from road.highway import Highway
from designer.op_states.default_state import DefaultState


# static function to get if left mouse button is pressed
def get_mouse_clicked():
    return pygame.mouse.get_pressed()[0]


# main designer class which acts as a context for our state objects
class Designer:
    SIM_FPS = 30  # simulator runs at 30 fps
    FPSTicker = pygame.time.Clock()  # create pygame fps clock

    def __init__(self):

        # set up pygame window rendering
        pygame.init()
        self.draw_surface = pygame.display.set_mode((1920, 900))
        self.draw_surface.fill((255, 255, 255))
        pygame.display.set_caption("Road Designer Self-driving #26")

        # initial title
        self.title = "ROAD DESIGNER"

        # buttons
        self.buttons = []
        self.init_menu()

        # create our highway
        self.highway = Highway(1, 40, (50, 870))

        # create default state
        self.designer_state = DefaultState(self)

        # this is used to check if we have to transition to another state set by self.designer_state
        self.designer_state_new = None

    # initialize menu buttons. Locations provided here are somewhat irrelevant since they are refreshed with new states.
    def init_menu(self):
        self.buttons.append(Button((10, 10), (70, 20), (255, 0, 0), "Add Lane", pygame.font.Font(None, 15),
                                   ButtonIdent.add_lane))
        self.buttons.append(Button((10, 40), (90, 20), (255, 0, 0), "Remove Lane", pygame.font.Font(None, 15),
                                   ButtonIdent.remove_lane))

        self.buttons.append(Button((10, 70), (120, 20), (255, 0, 0), "Choose Origin Point", pygame.font.Font(None, 15),
                                   ButtonIdent.select_origin))

        self.buttons.append(Button((10, 100), (120, 20), (255, 0, 0), "Add Straight Segment",
                                   pygame.font.Font(None, 15), ButtonIdent.add_straight_seg))

        self.buttons.append(Button((10, 130), (120, 20), (255, 0, 0), "Add Curved Segment",
                                   pygame.font.Font(None, 15), ButtonIdent.add_curve_seg))

        self.buttons.append(Button((10, 160), (120, 20), (255, 0, 0), "Edit segments", pygame.font.Font(None, 15),
                                   ButtonIdent.edit_segs))

        self.buttons.append(Button((10, 190), (120, 20), (255, 0, 0), "Finish Editing", pygame.font.Font(None, 15),
                                   ButtonIdent.complete_editing))

        self.buttons.append(Button((10, 220), (120, 20), (255, 0, 0), "Add On Ramp", pygame.font.Font(None, 15),
                                   ButtonIdent.add_entry_ramp))

        self.buttons.append(Button((10, 250), (120, 20), (255, 0, 0), "Complete On Ramp", pygame.font.Font(None, 15),
                                   ButtonIdent.complete_entry_ramp))

        self.buttons.append(Button((10, 250), (120, 20), (255, 0, 0), "Save Highway", pygame.font.Font(None, 15),
                                   ButtonIdent.save_highway))

    def draw_buttons(self):

        # draw buttons if they are visible. appropriate co-ordinates set by states
        for button in self.buttons:
            if button.is_visible:
                button.draw(self.draw_surface)

    def draw_title(self):
        txt_surface = pygame.font.Font(None, 25).render(self.title, True, (0, 0, 0))
        self.draw_surface.blit(txt_surface, (640, 10))

    def draw_highway(self):
        self.highway.draw_lanes(self.draw_surface)

    def run(self):
        run_designer = True
        while run_designer:
            for event in pygame.event.get():  # pass on events to the active state
                self.designer_state.handle_event(event)

                for button in self.buttons:  # pass on clicked buttons to the active state
                    if button.clicked(event) and event.type == pygame.MOUSEBUTTONUP:
                        self.designer_state.handle_click(button.ident)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if get_mouse_clicked():  # pass on mouse being clicked to the active state (never used)
                self.designer_state.handle_mouse_press(0)

            if self.designer_state_new is not None:  # update to new state requested by current state
                self.designer_state = self.designer_state_new
                self.designer_state_new = None

            # fill surface with white and draw items sequentially: title, buttons, highway, state-specific drawing
            self.draw_surface.fill((255, 255, 255))
            self.draw_title()
            self.draw_buttons()
            self.draw_highway()
            self.designer_state.draw(self.draw_surface)

            pygame.display.update()  # update the display and delay if necessary for locked FPS
            Designer.FPSTicker.tick(Designer.SIM_FPS)
