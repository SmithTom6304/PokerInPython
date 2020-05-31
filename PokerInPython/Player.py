import pygame

base_path = "./"


class Player:

    def __init__(self, number, chips, confidence, pos_x, pos_y):
        self.model = self.Model(number, chips, confidence)
        self.view = self.View(number, pos_x, pos_y)
        self.cards = [None, None]

    def get_number(self):
        return self.model.get_number()

    def get_chips(self):
        return self.model.get_chips()

    def get_confidence(self):
        return self.model.get_confidence()

    def get_image(self):
        return self.view.get_image()

    def get_rect(self):
        return self.view.get_rect()

    def move_to(self, x, y):
        self.view.move_absolute(x, y)

    def move_by(self, x, y):
        self.view.move_relative(x, y)

    def set_cards(self, cards):
        cards[0].move(self.view.rect.x + 20, self.view.rect.y + 120)
        cards[1].move(self.view.rect.x + 60, self.view.rect.y + 120)
        self.cards[0] = cards[0]
        self.cards[1] = cards[1]

    def get_cards(self):
        return self.cards

    # Returns true if the players cards are both face up, false if at least one is face down
    def is_cards_face_up(self):
        return self.get_cards()[0].isFaceUp() and self.get_cards()[1].isFaceUp()

    # Sets the players cards to be faceup/facedown based on value. Returns false if assertion fails
    def set_cards_face_up(self, value):
        return self.get_cards()[0].setFaceUp(value) and self.get_cards()[1].setFaceUp(value)

    def flip_cards(self):
        are_cards_face_up = self.is_cards_face_up()
        return self.set_cards_face_up(not are_cards_face_up)

    class Model:

        def __init__(self, number, chips, confidence):
            self.number = number
            self.chips = chips
            self.confidence = confidence

        def get_number(self):
            return self.number

        def get_chips(self):
            return self.chips

        def get_confidence(self):
            return self.confidence

    class View:

        def __init__(self, number, pos_x, pos_y):
            player_image_path = f"{base_path}Images/Characters/"
            self.image = pygame.image.load(f"{player_image_path}Player{number}.png")
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

        # Move a players rect coords to an absolute position
        def move_absolute(self, x, y):
            if x >= 0:
                self.rect.x = x
            else:
                self.rect.x = 0

            if y >= 0:
                self.rect.y = y
            else:
                self.rect.y = 0
