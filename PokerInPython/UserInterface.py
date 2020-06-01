# UserInterface layer
import pygame


class UserInterface:

    # myfont = pygame.font.SysFont('Elephant', 16)

    def __init__(self):
        self.size = self.width, self.height = 920, 640
        self.screen = None

        self.black = 0, 0, 0
        self.background = 49, 117, 61

        self.mouse_pos = 0, 0

    def init_display(self):
        self.screen = pygame.display.set_mode(self.size)

    def update_display(self, sequence):
        self.screen.fill(self.background)
        self.screen.blits(sequence)
        pygame.display.flip()
