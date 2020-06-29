import pygame
import Text

base_path = "./"


class Player:

    def __init__(self, number, chips, confidence, pos_x, pos_y):
        self.model = self.Model(number, chips, confidence)
        self.view = self.View(number, pos_x, pos_y)
        self.cards = [None, None]
        self.set_chips(chips)

    def get_number(self):
        return self.model.get_number()

    def get_chips(self):
        return self.model.get_chips()

    def set_chips(self, amount):
        self.model.set_chips(amount)
        self.view.update_text(amount)

    def get_confidence(self):
        return self.model.get_confidence()

    def get_image(self):
        return self.view.get_image()

    def get_rect(self):
        return self.view.get_rect()

    def get_text(self):
        return self.view.get_text()

    def get_text_rect(self):
        return self.view.get_text_rect()

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

    def get_chips_bet_in_round(self):
        return self.model.get_chips_bet_in_round()

    def set_chips_bet_in_round(self, value):
        self.model.chips_bet_in_round = value

    # Returns true if the players cards are both face up, false if at least one is face down
    def is_cards_face_up(self):
        return self.get_cards()[0].is_face_up() and self.get_cards()[1].is_face_up()

    # Sets the players cards to be faceup/facedown based on value. Returns false if assertion fails
    def set_cards_face_up(self, value):
        return self.get_cards()[0].set_face_up(value) and self.get_cards()[1].set_face_up(value)

    def flip_cards(self):
        are_cards_face_up = self.is_cards_face_up()
        return self.set_cards_face_up(not are_cards_face_up)

    def start_turn(self):
        self.view.image = pygame.transform.scale(self.view.image, (144+50, 200+50))

    def end_turn(self):
        self.view.image = pygame.transform.scale(self.view.image, (144, 200))

    def fold(self):
        self.model.set_folded(True)

    def has_folded(self):
        return self.model.get_folded()

    def reset(self):
        self.model.set_folded(False)
        self.cards = [None, None]
        self.end_turn()

    class Model:

        def __init__(self, number, chips, confidence):
            self.number = number
            self.chips: int = chips
            self.confidence = confidence
            self.folded = False
            self.chips_bet_in_round = 0

        def get_number(self):
            return self.number

        def get_chips(self):
            return self.chips

        def set_chips(self, amount):
            self.chips = amount

        def get_confidence(self):
            return self.confidence

        def get_folded(self):
            return self.folded

        def set_folded(self, value):
            self.folded = value

        def get_chips_bet_in_round(self):
            return self.chips_bet_in_round

        def set_chips_bet_in_round(self, value):
            self.chips_bet_in_round = value

    class View:

        black = (0, 0, 0)
        white = (255, 255, 255)

        def __init__(self, number, pos_x, pos_y):
            player_image_path = f"{base_path}Images/Characters/"
            self.image = pygame.image.load(f"{player_image_path}Player{number}.png")
            self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
            self.chips_text = None
            self.text = self.set_text()

        def set_text(self):
            text = Text.Text("Chips: -1", 32, self.black, None)
            return text

        def update_text(self, a_chip_count):
            self.text.set_text(f"Chips: {a_chip_count}")
            self.text.move_to(self.get_rect().x, self.get_rect().y - 20)

        def get_image(self):
            return self.image

        def get_rect(self):
            return self.rect

        def get_text(self):
            return self.text

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
