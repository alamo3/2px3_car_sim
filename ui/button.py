import pygame
from pygame.locals import *


class Button:

    def __init__(self, pos, size, color, text, font: pygame.font.Font):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        self.color = color
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.txt_surface = font.render(text, True, (0, 0, 0))

    def draw(self, surface):
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)

        return False
