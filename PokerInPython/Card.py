"""A module to provide implementation for cards.

...

Classes
-------
Card
    Implements a card. Requires an image file to draw from.

Methods
-------
None

"""

import pygame

base_path = "./"


class Card:
    """
    A class used to create a Card

    ...

    Attributes
    ----------
    model : Model
        An instance of the Model inner class, to keep track of the cards values.
    view : View
        An instance of the View inner class, to hold the card image and its rect.

    Methods
    -------
    update_position()
        Updates the cards position, if it's moving to a new position.
    get_value()
        Returns the cards value, as a dict {"number", "suit"}.
    is_face_up()
        Returns true if the card is face up.
    set_face_up(value)
        Set the card to be face up based on value.
    flip()
        Flip! Set the cards face up value to the opposite.
    get_image()
        Returns the cards image
    get_rect()
        Returns the cards rect
    is_moving()
        Returns whether the card is currently moving
    move(x, y)
        Make the card move towards (x, y)
    move_to(x, y)
        Move the card to (x, y)
    move_by(x, y)
        Move the card by (x, y)
    set_wait_frames(wait_frames)
        Set the cards wait_frames, stopping it from moving initially
    """

    def __init__(self, number: int, suit: str, pos_x: int = 0, pos_y: int = 0):
        """
        Parameters
        ----------
        :param number: Number value of the card
        :param suit: Suit of the card
        :param pos_x: x position of the card
        :param pos_y: y position of the card
        """
        self.model = self.Model(number, suit)
        # Return if failed to assign, most likely because card was assigned with bad values
        if self.model.get_value()["number"] is None or self.model.get_value()["suit"] is None:
            print("ERROR: Card was not initialized properly")
            return
        self.view = self.View(number, suit, pos_x, pos_y)

    def update_position(self):
        """Updates the cards position, if it's moving to a new position."""
        if self.view.move_step():
            self.model.moving = False

    def get_value(self):
        """Returns the cards value, as a dict {"number", "suit"}

        :return: The cards value
        """
        return self.model.get_value()

    def is_face_up(self):
        """Returns true if the card is face up

        :return: is_face_up: bool
        """
        return self.model.is_face_up()

    def set_face_up(self, value: bool):
        """Set the card to be face up based on value.

        :param value: bool
        :return: is_face_up: bool
        """
        self.view.set_image(value)
        return self.model.set_face_up(value)

    def flip(self):
        """Flip! Set the cards face up value to the opposite.

        :return: is_face_up: bool
        """
        flip_face_up = self.is_face_up()
        return self.set_face_up(not flip_face_up)

    def get_image(self):
        """Returns the cards image

        :return: image
        """
        return self.view.get_image()

    def get_rect(self):
        """Returns the cards rect

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

    def is_moving(self):
        """Returns whether the card is currently moving

        :return: is_moving: bool
        """
        return self.model.is_moving()

    def move(self, x: int, y: int):
        """Make the card move towards (x, y)

        :param x: x value to move to
        :param y: y value to move to
        """
        self.view.set_final_destination(x, y)
        self.model.moving = True

    def move_to(self, x: int, y: int):
        """Move the card to (x, y)

        :param x: x value to move to
        :param y: y value to move to
        """
        self.view.move_absolute(x, y)

    def move_by(self, x: int, y: int):
        """Move the card by (x, y)

        :param x: x value to move by
        :param y: y value to move by
        """
        self.view.move_relative(x, y)

    def set_wait_frames(self, wait_frames: int):
        """Set the cards wait_frames, stopping it from moving initially

        :param wait_frames: number of frames to wait for before moving
        """
        self.view.waitFrames = wait_frames

    class Model:
        """
        Inner class to keep track of cards values

        ...

        Attributes
        ----------
        value : {"number", "suit"}
            value of the card
        faceUp : bool
            name of the button
        moving : bool
            whether the card is currently moving

        Methods
        -------
        get_value()
            Returns the value of the card
        is_face_up()
            Returns true if the card is face up
        is_moving()
            Returns true if the card is moving
        set_face_up(value)
            Set faceUp to value
        set_moving(value)
            Set moving to value
        """

        def __init__(self, number: int, suit: str):
            """
            Parameters
            ---------
            :param number: number value of card
            :param suit: suit value of the card
            """
            self.value = {"number": None, "suit": None}
            self.faceUp = False
            self.moving = False

            # Ensure given card values are valid. Set to None and return if not.
            if number < 2 or number > 14:
                self.number = None
                return
            if suit not in ('H', 'D', 'C', 'S'):
                self.suit = None
                return

            self.value["number"] = number
            self.value["suit"] = suit

        def get_value(self):
            """Returns the value of the card

            :return: value: {"number", "suit"}
            """
            return self.value

        def is_face_up(self):
            """Returns true if the card is face up

            :return: faceUp: bool
            """
            return self.faceUp

        def is_moving(self):
            """Returns true if card is moving

            :return: moving
            """
            return self.moving

        def set_face_up(self, value: bool):
            """Set faceUp to value

            :param value: value to set faceUp to
            :return: Whether assignment succeeds: bool
            """
            if value is True:
                self.faceUp = True
                return True
            if value is False:
                self.faceUp = False
                return True
            return False  # If assignment fails, return false

        def set_moving(self, value: bool):
            """Set moving to value

            :param value: value to set moving to
            :return: Whether assignment succeeds: bool
            """
            if value is True:
                self.moving = True
                return True
            if value is False:
                self.moving = False
                return True
            return False  # If assignment fails, return false

    class View:
        """
        Inner class to keep track of cards display

        ...

        Attributes
        ----------
        imageFaceUp
            image to display when card is face up
        imageFaceDown
            image to display when card is face down
        image
            image to display
        rect
            cards rect
        waitFrames
            number of frames the card should stay still for before moving

        Methods
        -------
        set_image(face_up_value)
            Change image based on face_up_value
        get_image()
            Returns the cards image
        get_rect()
            Returns the cards rect
        move_relative(x, y)
            Move the card by (x, y)
        move_absolute(x, y)
            Move the card to (x, y)
        set_final_destination(x, y)
            Set the cards final destination to (x, y)
        move_step()
            Move the card a step towards it final destination
        """

        def __init__(self, number: int, suit: str, pos_x: int = 0, pos_y: int = 0, wait_frames: int = 0):
            """
            Parameters
            ----------
            :param number: Number value of the card
            :param suit: Suit value of the card
            :param pos_x: x position to set card to
            :param pos_y: y position to set card to
            :param wait_frames: Number of frames to wait before moving
            """
            card_image_path = f"{base_path}Images/Cards/"
            self.imageFaceUp = pygame.image.load(f"{card_image_path}Card_{number}{suit}.png")
            self.imageFaceDown = pygame.image.load(f"{card_image_path}Card_Back.png")
            self.image = self.imageFaceDown
            self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
            self.waitFrames = wait_frames

            self.movingTo = [0, 0]
            self.moving = False

        def set_image(self, face_up_value: bool):
            """Change image based on face_up_value

            :param face_up_value: Whether card is face up
            """
            if face_up_value is True:
                self.image = self.imageFaceUp
            else:
                self.image = self.imageFaceDown

        def get_image(self):
            """Returns the cards image

            :return: cards image
            """
            return self.image

        def get_rect(self):
            """Returns the cards rect

            :return: cards rect
            """
            return self.rect

        def move_relative(self, x: int, y: int):
            """Move the card by (x, y)

            :param x: x value to move card by
            :param y: y value to move card by
            """
            if (self.rect.x + x) >= 0:
                self.rect.x += x
            else:
                self.rect.x = 0

            if (self.rect.y + y) >= 0:
                self.rect.y += y
            else:
                self.rect.y = 0

        # Move a cards rect coords to an absolute position
        def move_absolute(self, x: int, y: int):
            """Move the card to (x, y)

            :param x: x value to move card to
            :param y: y value to move card to
            """
            if x >= 0:
                self.rect.x = x
            else:
                self.rect.x = 0

            if y >= 0:
                self.rect.y = y
            else:
                self.rect.y = 0

        def set_final_destination(self, x: int, y: int):
            """Set the cards final destination to (x, y)

            :param x: x value to move card towards
            :param y: y value to move card towards
            """
            if x >= 0:
                self.movingTo[0] = x
            else:
                self.movingTo[0] = 0

            if y >= 0:
                self.movingTo[1] = y
            else:
                self.movingTo[1] = 0

        def move_step(self):
            """Move the card a step towards it final destination

            :return: None
            """
            if self.waitFrames > 0:
                self.waitFrames -= 1
                return

            # Calculate difference between current pos and final pos
            a_rect = self.get_rect()
            a_move_to = self.movingTo
            delta_x = a_move_to[0] - a_rect.x
            delta_y = a_move_to[1] - a_rect.y
            step_size = 10

            # If x or y is close to final x or y, move it there
            if abs(delta_x) < step_size:
                self.move_absolute(a_move_to[0], a_rect.y)
            if abs(delta_y) < step_size:
                self.move_absolute(a_rect.x, a_move_to[1])

            if abs(delta_x) < step_size and abs(delta_y) < step_size:
                self.moving = False
                return True

            # Re-calculate difference between current pos and final pos
            a_rect = self.get_rect()
            a_move_to = self.movingTo
            delta_x = a_move_to[0] - a_rect.x
            delta_y = a_move_to[1] - a_rect.y

            # Move towards the final destination
            if delta_x > 0:
                self.move_relative(step_size, 0)
            if delta_x < 0:
                self.move_relative(-step_size, 0)
            if delta_y > 0:
                self.move_relative(0, step_size)
            if delta_y < 0:
                self.move_relative(0, -step_size)


