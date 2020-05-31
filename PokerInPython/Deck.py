import Card
import random
import pygame

base_path = "./"


class Deck:

    def __init__(self):
        deck_image_path = f"{base_path}Images/Cards/"
        self.deck = []
        self.image = pygame.image.load(f"{deck_image_path}Card_Deck.png")
        self.rect = self.image.get_rect(topleft=(100, 400))
        self.reset_deck()

    def reset_deck(self):

        self.deck.clear()

        for i in range(1, 14):
            self.deck.append(Card.Card(i, 'C', self.rect.x, self.rect.y))
        for i in range(1, 14):
            self.deck.append(Card.Card(i, 'D', self.rect.x, self.rect.y))
        for i in range(1, 14):
            self.deck.append(Card.Card(i, 'H', self.rect.x, self.rect.y))
        for i in range(1, 14):
            self.deck.append(Card.Card(i, 'S', self.rect.x, self.rect.y))

        self.shuffle_deck()

    # Function taken from https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/
    def shuffle_deck(self):

        arr = self.deck

        n = len(arr)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)

            arr[i], arr[j] = arr[j], arr[i]

        self.deck = arr

    def draw_card(self):
        return self.deck.pop()

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect
