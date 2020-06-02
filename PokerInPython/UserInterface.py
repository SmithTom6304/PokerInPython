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

    def check_button_presses(self, button_list):
        """Checks if a button is being pressed, and returns it

        :param button_list: List of buttons to check
        :return: Button being pressed. None if no button is pressed
        """
        if pygame.mouse.get_pressed()[0] is False:
            return None

        self.mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(button_list):
            if button.is_mouse_over(self.mouse_pos[0], self.mouse_pos[1]):
                return button
        return None
