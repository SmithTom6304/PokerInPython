# UserInterface layer
<<<<<<< HEAD
=======
import sys
>>>>>>> develop
import pygame

size = width, height = 920, 640
screen = None

black = 0, 0, 0
background = 49, 117, 61

mouse_pos = 0, 0

CardPath = "./Images/Cards/"
ButtonPath = "./Images/Buttons/"
CharacterPath = "./Images/Characters/"

cNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
cSuit = ['H', 'D', 'C', 'S']


# myfont = pygame.font.SysFont('Elephant', 16)

class Card:
    number = None
    suit = None

    image = None
    rect = None

    def __init__(self, number, suit, pos_x=0, pos_y=0):
        self.number = number
        self.suit = suit

        self.image = pygame.image.load(f"{CardPath}Card_{number}{suit}.png")
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def get_rect(self):
        return self.rect

    def get_number(self):
        return self.number

    def get_suit(self):
        return self.suit

    # Move a cards rect coords relative to the current coords
    def move_relative(self, x=0, y=0):
        if (self.rect.x + x) >= 0:
            self.rect.x += x
        else:
            self.rect.x = 0

        if (self.rect.y + y) >= 0:
            self.rect.y += y
        else:
            self.rect.y = 0

    # Move a cards rect coords to an absolute position
    def move_absolute(self, x=0, y=0):
        if x >= 0:
            self.rect.x = x
        else:
            self.rect.x = 0

        if y >= 0:
            self.rect.y = y
        else:
            self.rect.y = 0


class Opponent:
    rect = None
    image = None
    card = {"Card1": None, "Card2": None}
    chips = 100

    def __init__(self, x, y, number):
        self.image = pygame.image.load(f"{CharacterPath}Player{number}.png")
<<<<<<< HEAD
=======
        chips = 100
>>>>>>> develop
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_chips(self):
        return self.chips

    def get_rect(self):
        return self.rect

    def get_image(self):
        return self.image

    def get_cards(self):
        return self.card

<<<<<<< HEAD
=======
    def clear_cards(self):
        card = [None, None]

>>>>>>> develop

def init_display():
    global screen
    screen = pygame.display.set_mode(size)
    return


def update_display(sequence):
    screen.fill(background)

    screen.blits(sequence)

    pygame.display.flip()

    return


def player_mouse_over_card(card1, card2):
    if card1.rect.collidepoint(mouse_pos) and not card2.rect.collidepoint(mouse_pos):
        card1.move_relative(0, -10)

    if card2.rect.collidepoint(mouse_pos):
        card2.move_relative(0, -10)

    return
