"""
A module to implement text objects.
"""

import pygame

base_path = "./"
font_path = f"{base_path}Font/Minecraft.ttf"    # Set to path to use for font

class Text:

    def __init__(self, text_string, text_size, text_colour, text_background_colour):
        pygame.init()

        self.text_string = text_string
        self.text_size = text_size
        self.text_colour = text_colour
        self.text_background_colour = text_background_colour

        self.font = None
        self.text = None
        self.text_rect = None

        self.set_font()
        self.set_text(self.text_string)
        self.text_rect = self.text.get_rect()

    def set_font(self):
        self.font = pygame.font.Font(font_path, self.text_size)

    def set_text(self, a_text_string):
        self.text_string = a_text_string
        self.text = self.font.render(self.text_string, True, self.text_colour, self.text_background_colour)


    def move_to(self, pos_x, pos_y):
        if pos_x >= 0:
            self.text_rect.x = pos_x
        else:
            self.text_rect.x = 0

        if pos_y >= 0:
            self.text_rect.y = pos_y
        else:
            self.text_rect.y = 0

    def get_image(self):
        return self.text

    def get_rect(self):
        return self.text_rect

    def get_text_string(self):
        return self.text_string
"""
def update_text(self, a_chip_count):
    font = pygame.font.Font("Font/Minecraft.ttf", 32)
    self.chip_count = a_chip_count
    self.chips_text = f"Chips: {self.chip_count}"
    self.text = font.render(self.chips_text, True, self.black, None)
    self.text_rect = self.text.get_rect()
    self.text_rect.center = self.get_rect().center
    self.text_rect.y -= 120
"""