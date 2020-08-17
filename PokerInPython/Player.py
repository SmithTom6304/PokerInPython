import pygame
import Text

base_path = "./"


class Player:

    def __init__(self, number, chips, confidence, pos_x, pos_y):
        self.model = self.Model(number, chips)
        self.view = self.View(number, pos_x, pos_y)
        self.cards = [None, None]
        self.set_chips(chips)

    def get_number(self) -> int:
        """
        Get the players number

        :return: int: The players number

        """
        return self.model.get_number()

    def get_chips(self) -> int:
        """
        Returns the number of chips the player has

        :return: int: The players chip amount
        """
        return self.model.get_chips()

    def set_chips(self, amount: int):
        """
        Set the amount of chips a player has

        :param amount: Number of chips
        """
        self.model.set_chips(amount)
        self.view.update_text(amount, number=self.get_number())

    def get_image(self):
        """
        Returns the players image

        :return: The players image

        """
        return self.view.get_image()

    def get_rect(self):
        """
        Returns the players rect object

        :return: The players rect object

        """
        return self.view.get_rect()

    def get_text(self):
        """
        Return the players text object

        :return: The players text object
        """
        return self.view.get_text()

    def get_text_rect(self):
        """
        Returns the rect of the players text object

        :return: The rect of the players text object

        """
        return self.view.get_text_rect()

    def move_to(self, x: int, y: int):
        """
        Move the player to x, y

        :param x: x coordinate to move to
        :param y: y coordinate to move to
        """
        self.view.move_absolute(x, y)

    def move_by(self, x: int, y: int):
        """
        Move the player by x, y

        :param x: Amount to move the player in the x direction
        :param y: Amount to move the player in the y direction
        """
        self.view.move_relative(x, y)

    def set_cards(self, cards: list):
        """
        Set the players cards

        :param cards: List of cards [card, card]
        """
        cards[0].move(self.view.rect.x + 20, self.view.rect.y + 120)
        cards[1].move(self.view.rect.x + 60, self.view.rect.y + 120)
        self.cards[0] = cards[0]
        self.cards[1] = cards[1]

    def get_cards(self) -> list:
        """
        Get the players cards

        :return: List of players cards [card, card]

        """
        return self.cards

    def change_cards(self, old_card, new_card):
        """
        Swap one of the players cards with a new one

        :param old_card: The players card to be replaced
        :param new_card: The card to be replaced with

        :return: True if the swap was successful

        """
        if self.cards[0] == old_card:
            self.cards[0] = new_card
            self.set_cards(self.cards)
            return True
        if self.cards[1] == old_card:
            self.cards[1] = new_card
            self.set_cards(self.cards)
            return True

    def get_chips_bet_in_round(self) -> int:
        """
        Return the amount of chips the player has bet in the current round

        :return: Amount of chips the player has bet in the current round
        """
        return self.model.get_chips_bet_in_round()

    def set_chips_bet_in_round(self, value):
        """
        Sets the amount of chips the player has bet in the current round

        :param value: The amount of chips the player has bet in the current round
        """
        self.model.chips_bet_in_round = value

    def is_cards_face_up(self) -> bool:
        """
        Return true if both the players cards are face up

        :return: true if both the players cards are face up

        """
        return self.get_cards()[0].is_face_up() and self.get_cards()[1].is_face_up()

    # Sets the players cards to be faceup/facedown based on value. Returns false if assertion fails
    def set_cards_face_up(self, value: bool) -> bool:
        """
        Set the players cards to be faceup/facedown (true/false)

        :param value: Whether to set cards faceup (true) or facedown (false)

        :return: true if the cards are set successfully

        """
        return self.get_cards()[0].set_face_up(value) and self.get_cards()[1].set_face_up(value)

    def flip_cards(self):
        """
        Flip the cards, reversing their faceup values

        :return: true if the cards are set successfully

        """
        are_cards_face_up = self.is_cards_face_up()
        return self.set_cards_face_up(not are_cards_face_up)

    def start_turn(self):
        """
        Method called when a player begins their turn.
        Sets the players image to a larger version.

        """
        if self.get_number() == 1:
            return
        try:
            self.view.set_image(f"Player{self.get_number()}Active")
        except RuntimeError as e:
            print(e)
            print("Scaling image instead")
            self.view.image = pygame.transform.scale(self.view.image, (144+50, 200+50))

    def end_turn(self):
        """
        Method called when a player ends their turn.
        Sets the players image back to normal size.

        """
        if self.get_number() == 1:
            return
        try:
            self.view.set_image(f"Player{self.get_number()}")
        except RuntimeError as e:
            print(e)
            print("Scaling image instead")
            self.view.image = pygame.transform.scale(self.view.image, (144, 200))

    def has_lost(self) -> bool:
        """
        Returns true if the player is out of the game.

        :return: true if the player is out of the game.

        """
        return self.model.get_has_lost()

    def set_has_lost(self, value: bool):
        """
        Set whether the player has lost the game

        :param value: has_lost value
        """
        self.model.set_has_lost(value)

    def fold(self, has_cards=True):
        """
        Fold the players hand

        :param has_cards: Whether the player has cards. Used when a player is out of the game,
        and so has not been dealt cards. Required since we move the players cards down when they fold.

        """
        # TODO use a try catch loop instead of requiring a parameter
        self.model.set_folded(True)
        if has_cards:
            self.cards[0].move_by(0, 20)
            self.cards[1].move_by(0, 20)

    def has_folded(self) -> bool:
        """
        Return true if the player has folded

        :return: true if the player has folded

        """
        return self.model.get_folded()

    def reset(self):
        """
        Set the player back to default values to begin a new round

        """
        self.model.set_folded(False)
        self.cards = [None, None]
        self.end_turn()

    class Model:

        def __init__(self, number, chips):
            self.number = number
            self.chips: int = chips
            self.folded = False
            self.chips_bet_in_round = 0
            self.has_lost = False

        def get_number(self):
            return self.number

        def get_chips(self):
            return self.chips

        def set_chips(self, amount):
            self.chips = amount

        def get_folded(self):
            return self.folded

        def set_folded(self, value):
            self.folded = value

        def set_has_lost(self, value: bool):
            self.has_lost = value

        def get_has_lost(self):
            return self.has_lost

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

        def update_text(self, a_chip_count, number: int):
            self.text.set_text(f"Chips: {a_chip_count}")
            if number == 1:
                self.text.move_to(self.get_rect().x, self.get_rect().y + 63)
            else:
                self.text.move_to(self.get_rect().x, self.get_rect().y - 30)

        def get_image(self):
            return self.image

        def set_image(self, image_path):
            player_image_path = f"{base_path}Images/Characters/"
            try:
                self.image = pygame.image.load(f"{player_image_path}{image_path}.png")
            except Exception:
                raise RuntimeError(f"Failed to load image with path '{player_image_path}{image_path}.png'")

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
