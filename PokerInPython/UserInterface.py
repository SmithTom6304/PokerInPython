"""
A module to handle drawing the game screen

Classes
-------
UserInterface
    Draws and updates the user interface, and handles player input

Methods
-------
None
"""

import pygame


class UserInterface:

    def __init__(self):
        """
        Attributes
        ----------
            self.size: The width and height of the screen
            self.screen: The screen object to draw to
            self.background: The background image
            self.mouse_pos: The x,y coordinates of the mouse

        """
        self.size = self.width, self.height = 920, 640
        self.screen = None
        self.background = pygame.image.load("./Images/Menu.png")
        self.mouse_pos = 0, 0

    def init_display(self):
        """Initialize the screen object

        """
        self.screen = pygame.display.set_mode(self.size)

    def update_display(self, sequence):
        """
        Draw a sequence of objects to the display

        Parameters
        ----------
        sequence
            A sequence of tuples of type (image, rect) to be drawn to the screen
        """
        self.screen.blit(self.background, (0, 0))
        self.screen.blits(sequence)
        pygame.display.flip()

    def check_button_presses(self, button_list):
        """Checks if a button is being pressed, and returns it

        :param button_list: List of buttons to check
        :return: Button being pressed. None if no button is pressed
        """
        pygame.event.get()

        if pygame.mouse.get_pressed()[0] is False:
            return None

        self.mouse_pos = pygame.mouse.get_pos()
        # button is a list of tuples (index, button)
        for button in enumerate(button_list):
            if button[1].is_mouse_over(self.mouse_pos[0], self.mouse_pos[1]):
                return button[1]
        return None

    def check_card_presses(self, card_list):
        """
        Checks if a card is being clicked on, and returns it

        Parameters
        ----------
        card_list
            List of cards to be checked

        Returns
        -------
        Card
            The card being clicked on

        """
        pygame.event.get()

        if pygame.mouse.get_pressed()[0] == 0:
            return None

        self.mouse_pos = pygame.mouse.get_pos()
        # button is a list of tuples (index, button)
        for card in enumerate(card_list):
            if card[1].is_mouse_over(self.mouse_pos[0], self.mouse_pos[1]):
                return card[1]
        return None

    def show_card_menu(self, deck_object):
        """
        Display a menu to swap cards, to help with debugging

        Parameters
        ----------
        deck_object
            Deck object containing all the cards that can be swapped with

        Returns
        -------
            Card being swapped with

        """
        deck = deck_object.deck
        draw_sequence = []
        # a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
        deck.sort(key=lambda x: (x.get_value()["suit"], x.get_value()["number"]))

        padding = [20, 20]
        a_card = deck[0]
        a_card_rect = a_card.get_rect()
        card_width = a_card_rect.width
        card_height = a_card_rect.height
        screen_width = self.width
        cards_in_row = int(screen_width / card_width)

        for i, card in enumerate(deck):
            column = i % cards_in_row
            row = int(i / cards_in_row)

            card.move_to(column * card_width + padding[0], row * card_height + padding[1])
            card.set_face_up(True)
            draw_sequence.append((card.get_image(), card.get_rect()))

        self.screen.fill((153, 204, 255))
        self.screen.blits(draw_sequence)
        pygame.display.flip()

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            card_pressed = self.check_card_presses(deck)
            if card_pressed is not None:
                for card in deck:
                    card.move_to(deck_object.rect.x, deck_object.rect.y)
                return card_pressed
            clock.tick(60)

    def change_background(self, a_background: str):
        """
        Change the background image

        Parameters
        ----------
        a_background
            What background should be swapped to
            "UI": The user interface background
            "Menu": The main menu background

        """
        bg_ui = "./Images/UI.png"
        bg_menu = "./Images/Menu.png"

        if a_background == "UI":
            self.background = pygame.image.load(bg_ui)
        elif a_background == "Menu":
            self.background = pygame.image.load(bg_menu)
