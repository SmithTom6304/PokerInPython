import sys
import pygame
import os

import UserInterface
# import Card
import Player
import Deck
import Button

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 35)

class PokerInPython:

    size = width, height = 920, 640
    speed = [2, 2]
    black = 0, 0, 0
    background = 49, 117, 61

    # Queue of objects to be added to the sequence to update
    objectImagesToUpdateQueue = []
    # List of (image, rect) tuples to provide to UserInterface layer to update screen
    objectImagesToUpdateSequence = [None, None]

    playerList = []
    buttonList = []
    cardList = []
    communityCards = []




    def __init__(self):
        self.deck = Deck.Deck()
        self.user_interface = UserInterface.UserInterface()


    def handle_events(self):
        button_pressed = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.initialize_game_objects()
                if event.key == pygame.K_RIGHT:
                    for each in self.cardList:
                        each.set_face_up(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check button presses
                button_pressed = self.user_interface.check_button_presses(self.buttonList)

        mouse_pos = pygame.mouse.get_pos()
        self.user_interface.mouse_pos = mouse_pos

        if button_pressed is not None:
            print(button_pressed.get_name())  # TODO Change to button function
            return button_pressed


    def initialize_game_objects(self):
        self.playerList.clear()
        self.buttonList.clear()
        self.cardList.clear()
        self.communityCards.clear()
        self.deck.reset_deck()

        self.initialize_players(4, 100)
        self.initialize_buttons()
        # initialize_cards()

        # Add wait frames to each card to create ripple effect
        for i, card in enumerate(self.cardList):
            card.set_wait_frames((len(self.cardList) - i) * 3)


    def initialize_players(self, number_of_players, chips):
        player1 = Player.Player(1, chips, confidence=100, pos_x=80, pos_y=400)
        player1.set_cards([self.deck.draw_card(), self.deck.draw_card()])
        player1.set_cards_face_up(True)
        self.playerList.append(player1)
        self.cardList.extend(player1.get_cards())

        for i in range(2, number_of_players + 1):
            x_value = (self.width / number_of_players) * (i - 1)
            player = Player.Player(i, chips, confidence=100, pos_x=x_value, pos_y=(self.height / 6))
            player.set_cards([self.deck.draw_card(), self.deck.draw_card()])
            self.playerList.append(player)
            self.cardList.extend(player.get_cards())




    def initialize_buttons(self):
        btn1 = Button.Button(button_id=1, name="Fold", pos_x=500, pos_y=540)
        btn2 = Button.Button(button_id=2, name="Check", pos_x=640, pos_y=540)
        btn3 = Button.Button(button_id=3, name="Bet", pos_x=780, pos_y=540)

        self.buttonList.append(btn1)
        self.buttonList.append(btn2)
        self.buttonList.append(btn3)


    def initialize_cards(self):
        test_card = self.deck.draw_card()
        test_card.move_to(100, 100)
        test_card.move(600, 400)
        self.cardList.append(test_card)

    def deal_community_cards(self, phase):
        if phase == 1:
            return
        if phase == 2:
            for i in range(0, 3):
                card = self.deck.draw_card()
                card.set_wait_frames(i * 3)
                card.move(200 + (100 * (i+1)), 400)
                card.set_face_up(True)
                self.communityCards.append(card)
                self.cardList.append(card)
        if phase == 3:
            card = self.deck.draw_card()
            card.move(200 + (100 * (3 + 1)), 400)
            card.set_face_up(True)
            self.communityCards.append(card)
            self.cardList.append(card)
        if phase == 4:
            card = self.deck.draw_card()
            card.move(200 + (100 * (4 + 1)), 400)
            card.set_face_up(True)
            self.communityCards.append(card)
            self.cardList.append(card)





    def game_loop(self, leadPosition, turn, button_pressed):
        index = leadPosition + turn % len(self.playerList)
        current_player = self.playerList[index]

        action = button_pressed.get_name()

        if action == "Fold":
            print(f"Player {index} folded")
            return


    def update(self):
        # Clear the sequence of images that will be updated
        self.objectImagesToUpdateSequence.clear()
        self.objectImagesToUpdateQueue.clear()

        for player in self.playerList:
            self.objectImagesToUpdateQueue.append(player)
        # objectImagesToUpdateQueue.extend(player.getCards())

        for button in self.buttonList:
            self.objectImagesToUpdateQueue.append(button)

        for card in self.cardList:
            if card.is_moving():
                card.move_step()

            self.objectImagesToUpdateQueue.append(card)

        self.objectImagesToUpdateQueue.append(self.deck)

        for each in self.objectImagesToUpdateQueue:
            self.objectImagesToUpdateSequence.append((each.get_image(), each.get_rect()))

        self.user_interface.update_display(self.objectImagesToUpdateSequence)

    def main(self):
        pygame.init()
        clock = pygame.time.Clock()

        self.user_interface.init_display()

        self.initialize_game_objects()
        lead_position = 0
        turn = 0
        phase = 1  # https://www.poker-king.com/dictionary/community_cards/
        # Phase 1 - Deal private cards, then bet
        # Phase 2 - Deal three community cards to form the flop, then bet
        # Phase 3 - Deal fourth community card, called the turn, then bet
        # Phase 4 - Deal last community card, called the river, then bet
        # Showdown - show cards

        while True:
            button_pressed = self.handle_events()
            if button_pressed is not None:
                if lead_position == (turn + 1) % len(self.playerList):
                    phase += 1
                    print(f"Starting phase {phase}")
                    self.deal_community_cards(phase)
                self.game_loop(lead_position, turn, button_pressed)
                turn = (turn + 1) % len(self.playerList)

            self.update()
            clock.tick(60)


if __name__ == '__main__':
    game = PokerInPython()
    game.main()
