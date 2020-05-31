import pygame

base_path = "./"


class Button:

    def __init__(self, button_id, name, pos_x=0, pos_y=0):
        self.model = self.Model(button_id, name)
        self.view = self.View(name, pos_x, pos_y)

    def get_button_id(self):
        return self.model.get_button_id()

    def get_name(self):
        return self.model.get_name()

    def move_to(self, x, y):
        self.view.move_absolute(x, y)

    def move_by(self, x, y):
        self.view.move_relative(x, y)

    def get_image(self):
        return self.view.get_image()

    def get_rect(self):
        return self.view.get_rect()

    class Model:
        def __init__(self, button_id, name):
            self.button_id = button_id
            self.name = name

        def get_button_id(self):
            return self.button_id

        def get_name(self):
            return self.name

    class View:
        def __init__(self, name, pos_x, pos_y):

            button_image_path = f"{base_path}Images/Buttons/"

            self.image = pygame.image.load(f"{button_image_path}Btn_{name}.png")
            self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

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

        # Move a buttons rect coords to an absolute position
        def move_absolute(self, x, y):
            if x >= 0:
                self.rect.x = x
            else:
                self.rect.x = 0

            if y >= 0:
                self.rect.y = y
            else:
                self.rect.y = 0
