import pygame

base_path = "./"


class Card:

    def __init__(self, number, suit, pos_x=0, pos_y=0):
        self.model = self.Model(number, suit)
        # Return if failed to assign, most likely because card was assigned with bad values
        if self.model.get_value()["number"] is None or self.model.get_value()["suit"] is None:
            print("ERROR: Card was not initialized properly")
            return
        self.view = self.View(number, suit, pos_x, pos_y)

    def update_position(self):
        self.move_step()

    def get_value(self):
        return self.model.get_value()

    # Returns true if the card is face up
    def is_face_up(self):
        return self.model.is_face_up()

    # Sets the card to be faceup/facedown based on value. Returns false if assertion fails
    def set_face_up(self, value):
        self.view.set_image(value)
        return self.model.set_face_up(value)

    def flip(self):
        flip_faceup = self.is_face_up()
        return self.set_face_up(not flip_faceup)

    def get_image(self):
        return self.view.get_image()

    def get_rect(self):
        return self.view.get_rect()

    def is_moving(self):
        return self.model.is_moving()

    def move(self, x, y):
        self.view.new_move_absolute(x, y)
        self.model.moving = True

    def move_to(self, x, y):
        self.view.move_absolute(x, y)

    def move_by(self, x, y):
        self.view.move_relative(x, y)

    def move_step(self):
        self.view.move_step()

    def set_wait_frames(self, wait_frames):
        self.view.waitFrames = wait_frames

    class Model:

        def __init__(self, number, suit):
            self.value = {"number": None, "suit": None}
            self.faceUp = False
            self.moving = False

            # Ensure given card values are valid. Set to None and return if not.
            if number < 1 or number > 13:
                self.number = None
                return
            if suit not in ('H', 'D', 'C', 'S'):
                self.suit = None
                return

            self.value["number"] = number
            self.value["suit"] = suit

        def get_value(self):
            return self.value

        def is_face_up(self):
            return self.faceUp

        def is_moving(self):
            return self.moving

        def set_face_up(self, value):
            if value is True:
                self.faceUp = True
                return True
            if value is False:
                self.faceUp = False
                return True
            return False  # If assignment fails, return false

        def set_moving(self, value):
            if value is True:
                self.moving = True
                return True
            if value is False:
                self.moving = False
                return True
            return False  # If assignment fails, return false

    class View:

        def __init__(self, number, suit, pos_x=0, pos_y=0, wait_frames=0):
            card_image_path = f"{base_path}Images/Cards/"
            self.imageFaceUp = pygame.image.load(f"{card_image_path}Card_{number}{suit}.png")
            self.imageFaceDown = pygame.image.load(f"{card_image_path}Card_Back.png")
            self.image = self.imageFaceDown
            self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
            self.waitFrames = wait_frames

            self.movingTo = [0.0, 0.0]
            self.moving = False

        def set_image(self, face_up_value):
            if face_up_value is True:
                self.image = self.imageFaceUp
            else:
                self.image = self.imageFaceDown

        def get_image(self):
            return self.image

        def get_rect(self):
            return self.rect

        def move_relative(self, x, y):

            if (self.rect.x + x) >= 0:
                self.rect.x += x
            else:
                self.rect.x = 0

            if (self.rect.y + y) >= 0:
                self.rect.y += y
            else:
                self.rect.y = 0

        # Move a cards rect coords to an absolute position
        def move_absolute(self, x, y):
            if x >= 0:
                self.rect.x = x
            else:
                self.rect.x = 0

            if y >= 0:
                self.rect.y = y
            else:
                self.rect.y = 0

        def new_move_absolute(self, x, y):
            if x >= 0:
                self.movingTo[0] = x
            else:
                self.movingTo[0] = 0

            if y >= 0:
                self.movingTo[1] = y
            else:
                self.movingTo[1] = 0

        def move_step(self):

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

            if delta_x == 0 and delta_y == 0:
                self.moving = False
