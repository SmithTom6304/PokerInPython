"""A module to provide implementation for buttons.

...

Classes
-------
Button
    Implements a button. Requires an image file to draw from.

Methods
-------
None

"""

import pygame

base_path = "./"


class Button:
    """
    A class used to create a Button

    ...

    Attributes
    ----------
    model : Model
        An instance of the Model inner class, to keep track of the buttons values.
    view : View
        An instance of the View inner class, to hold the button image and its rect.

    Methods
    -------
    get_button_id()
        Returns the buttons id
    get_name()
        Returns the buttons name
    move_to(x, y)
        Moves the button to (x, y)
    move_by(x, y)
        Moves the button by (x, y)
    get_image()
        Returns the buttons image
    get_rect()
        Returns the buttons rect
    """
    def __init__(self, button_id: int, name: str, pos_x: int = 0, pos_y: int = 0):
        """
        Parameters
        ----------
        :param button_id: Id of the button.
        :param name: Name of the button. Used to find the image of the button.
        :param pos_x: x position to move button to
        :param pos_y: y position to move button to
        """
        self.model = self.Model(button_id, name)
        self.view = self.View(name, pos_x, pos_y)

    def get_button_id(self):
        """Returns the buttons id.

        :return: button_id : int
        """
        return self.model.get_button_id()

    def get_name(self):
        """Returns the buttons name

        :return: name : str
        """
        return self.model.get_name()

    def move_to(self, x: int, y: int):
        """Moves the button to (x, y)

        :param x: x value to move to.
        :param y: y value to move to.
        """
        self.view.move_absolute(x, y)

    def move_by(self, x: int, y: int):
        """Moves the button by (x, y)

        :param x: value to move along x axis
        :param y: value to move along y axis
        """
        self.view.move_relative(x, y)

    def get_image(self):
        """Returns the buttons image

        :return: image
        """
        return self.view.get_image()

    def get_rect(self):
        """Returns the buttons rect

        :return: rect
        """
        return self.view.get_rect()

    def is_mouse_over(self, mouse_x, mouse_y):
        """Returns true if the mouse is over the button

        :param mouse_x: x position of the mouse
        :param mouse_y: y position of the mouse
        :return: True if mouse is over the button
        """
        a_rect = self.get_rect()
        return a_rect.collidepoint(mouse_x, mouse_y)

    def change_button(self, name):
        self.model.name = name
        self.view.name = name
        self.view.set_image(name)

    class Model:
        """
        Inner class to keep track of buttons values

        ...

        Attributes
        ----------
        button_id : int
            numeric id of the button
        name : str
            name of the button

        Methods
        -------
        get_button_id()
            Returns the buttons id
        get_name()
            Returns the buttons name
        """
        def __init__(self, button_id, name):
            """
            Parameters
            ----------
            :param button_id: id of the button
            :param name: name of the button
            """
            self.button_id = button_id
            self.name = name

        def get_button_id(self):
            """Returns the buttons id

            :return: button_id : int
            """
            return self.button_id

        def get_name(self):
            """Returns the buttons name

            :return: name : str
            """
            return self.name

    class View:
        """
        Inner class to keep track of buttons display

        ...

        Attributes
        ----------
        image
            button image to be displayed
        rect
            buttons rect

        Methods
        -------
        get_image()
            Returns the buttons image
        get_rect()
            Returns the buttons rect
        move_relative(x, y)
            Moves the button by (x, y)
        move_absolute(x, y)
            Moves the button to (x, y)
        """
        def __init__(self, name, pos_x, pos_y):
            """
            Parameters
            ----------
            :param name: Name of the button. Used to find the image
            :param pos_x: x value of the button
            :param pos_y: y value of the button
            """

            self.image = None
            self.set_image(name)
            self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        def set_image(self, name):
            button_image_path = f"{base_path}Images/Buttons/"
            image = pygame.image.load(f"{button_image_path}Btn_{name}.png")
            self.image = image

        def get_image(self):
            """Returns the buttons image

            :return: image
            """
            return self.image

        def get_rect(self):
            """Returns the buttons rect

            :return: rect
            """
            return self.rect

        def move_relative(self, x, y):
            """Move the button by (x, y)

            :param x: Amount to move button along x axis
            :param y: Amount to move button along y axis
            """
            if (self.rect.x + x) >= 0:
                self.rect.x += x
            else:
                self.rect.x = 0

            if (self.rect.y + y) >= 0:
                self.rect.y += y
            else:
                self.rect.y = 0

        # Move a buttons rect coords to an absolute position
        def move_absolute(self, x, y):
            """Move the button to (x, y)

            :param x: x coordinate to move button to
            :param y: y coordinate to move button to
            """
            if x >= 0:
                self.rect.x = x
            else:
                self.rect.x = 0

            if y >= 0:
                self.rect.y = y
            else:
                self.rect.y = 0
