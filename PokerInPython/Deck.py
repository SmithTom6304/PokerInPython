"""A module to provide implementation of a deck.

...

Classes
-------
Deck
    Implements a deck. Requires an image file to draw from.

Methods
-------
None

"""

import Card
import random
import pygame

base_path = "./"


class Deck:
    """
    A class used to create a Deck

    ...

    Attributes
    ----------
    deck : list
        A list of cards.
    image
        Picture to display
    rect
        Decks rect

    Methods
    -------
    reset_deck()
        Reset and reshuffle the deck.
    shuffle_deck()
        Shuffle the deck.
    draw_card()
        Return the top card.
    get_image()
        Return the cards image
    get_rect()
        Return the cards rect
    """

    def __init__(self):
        deck_image_path = f"{base_path}Images/Cards/"
        self.deck = []
        self.image = pygame.image.load(f"{deck_image_path}Card_Deck.png")
        self.rect = self.image.get_rect(topleft=(100, 400))
        self.reset_deck()

    def reset_deck(self):
        """
        Reset and reshuffle the deck.
        """
        self.deck.clear()

        for i in range(2, 15):
            self.deck.append(Card.Card(i, 'D', self.rect.x, self.rect.y))
        for i in range(2, 15):
            self.deck.append(Card.Card(i, 'C', self.rect.x, self.rect.y))
        for i in range(2, 15):
            self.deck.append(Card.Card(i, 'H', self.rect.x, self.rect.y))
        for i in range(2, 15):
            self.deck.append(Card.Card(i, 'S', self.rect.x, self.rect.y))

        self.shuffle_deck()

    # Function taken from https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/
    def shuffle_deck(self):
        """
        Shuffle the deck.
        """
        arr = self.deck

        n = len(arr)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)

            arr[i], arr[j] = arr[j], arr[i]

        self.deck = arr

    def draw_card(self):
        """
        Return the top card.
        :return: Card
        """
        return self.deck.pop()

    def remove_card(self, a_card):
        self.deck.remove(a_card)

    def insert_card(self, a_card, shuffle=True):
        self.deck.insert(0, a_card)
        if shuffle:
            self.shuffle_deck()

    def get_image(self):
        """
        Return the cards image
        :return: Deck image
        """
        return self.image

    def get_rect(self):
        """
        Return the cards rect
        :return: Deck rect
        """
        return self.rect
