"""
A module to implement text objects.
"""

import pygame
import time

base_path = "./"
font_path = f"{base_path}Font/Minecraft.ttf"  # Set to path to use for font


class Text:
    """
    A class used to display Text

    ...

    Attributes
    ----------
    text_string : str
        The text to display
    text_size : int
        Size of the text
    text_colour : (int, int, int)
        RGB value of the text colour
    text_background_colour : (int, int, int)
        RHB value of the background colour. Set to None for transparent.
    font
        Font object of the text
    text
        The text object
    text_rect
        Rect of the text

    Methods
    -------
    set_font()
        Sets the font based on the font_path and text_size
    set_text(text_string)
        Sets the text to display to the given text_string
    move_to(x, y)
        Move the text to the given x and y coords
    get_image()
        Returns the text object
    get_rect()
        Returns the rect object
    get_text_string()
        Returns the text_string.
    """
    def __init__(self, text_string, text_size, text_colour, text_background_colour):
        """
        Parameters
        ----------
        :param text_string: str
        :param text_size: int
        :param text_colour: (int, int, int). None for transparent
        :param text_background_colour: (int, int, int). None for transparent
        """
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
        self.timer = 0.0

    def set_font(self):
        """
        Sets the font based on the font_path and text_size
        """
        self.font = pygame.font.Font(font_path, self.text_size)

    def set_text(self, a_text_string):
        """
        Sets the text to display to the given text_string
        :param a_text_string: str
        """
        self.text_string = a_text_string
        self.text = self.font.render(self.text_string, True, self.text_colour, self.text_background_colour)

    def move_to(self, pos_x, pos_y):
        """
        Move the text to the given x and y coords
        :param pos_x: int
        :param pos_y: int
        """
        if pos_x >= 0:
            self.text_rect.x = pos_x
        else:
            self.text_rect.x = 0

        if pos_y >= 0:
            self.text_rect.y = pos_y
        else:
            self.text_rect.y = 0

    def get_image(self):
        """
        Returns the text object
        :return: Text object
        """
        return self.text

    def get_rect(self):
        """
        Returns the rect object
        :return: Rect object
        """
        return self.text_rect

    def get_text_string(self):
        """
        Returns the text_string.
        :return: str
        """
        return self.text_string

    def set_timer(self, t: float):
        self.timer = time.time() + t

    def check_timer(self):
        if self.timer == 0:
            return False
        if time.time() > self.timer:
            self.timer = 0
            return True
        return False




