import sys
import pygame
import os

import UserInterface
# import Card
import Player
import Deck
import Button
import Text

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
    textObjectList = []

    communityCards = []


    def __init__(self):
        self.pot = Pot()
        self.deck = Deck.Deck()
        self.user_interface = UserInterface.UserInterface()

        self.start_lead_position = 0
        self.lead_position = 0
        self.turn = 0
        self.big_blind = -1
        self.small_blind = -1
        self.phase = 1  # https://www.poker-king.com/dictionary/community_cards/
        # Phase 1 - Deal private cards, then bet
        # Phase 2 - Deal three community cards to form the flop, then bet
        # Phase 3 - Deal fourth community card, called the turn, then bet
        # Phase 4 - Deal last community card, called the river, then bet
        # Showdown - show cards
        self.current_player: Player.Player = None

    # ---INPUT HANDLING---
    def handle_events(self):
        """Handle input events

        :return: Button pressed
        """
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
            return button_pressed
    # --------------------

    # ---INITIALIZE OBJECTS---
    def initialize_game_objects(self, initialize_players=True):
        if initialize_players is True:
            self.playerList.clear()

        self.buttonList.clear()
        self.cardList.clear()
        self.textObjectList.clear()
        self.communityCards.clear()
        self.deck.reset_deck()
        self.pot.pot = 0  # TODO Change to pot.reset

        self.phase = 1
        if initialize_players is True:
            self.initialize_players(4, 100)


        for player in self.playerList:
            player.reset()
            self.textObjectList.append(player.get_text())

        self.initialize_cards()
        self.initialize_buttons()
        # initialize_cards()

        # Add wait frames to each card to create ripple effect
        for i, card in enumerate(self.cardList):
            card.set_wait_frames((len(self.cardList) - i) * 3)

        self.round_initialization()

    def round_initialization(self):
        self.lead_position = self.start_lead_position
        self.start_lead_position = (self.start_lead_position + 1) % len(self.playerList)
        self.turn = self.lead_position
        self.current_player = self.playerList[self.lead_position]
        self.current_player.start_turn()

        self.big_blind = self.lead_position - 1
        self.small_blind = self.lead_position - 2
        if self.big_blind < 0:
            self.big_blind += len(self.playerList)
        if self.small_blind < 0:
            self.small_blind += len(self.playerList)

        self.pot.bet_blinds(self.playerList[self.big_blind], self.playerList[self.small_blind])

        self.pot.set_min_bet(self.pot.bet_amount)

    def initialize_players(self, number_of_players, chips):
        player1 = Player.Player(1, chips, confidence=100, pos_x=80, pos_y=400)
        self.playerList.append(player1)

        for i in range(2, number_of_players + 1):
            x_value = (self.width / number_of_players) * (i - 1)
            player = Player.Player(i, chips, confidence=100, pos_x=x_value, pos_y=(self.height / 6))
            self.playerList.append(player)

        self.current_player = self.playerList[0]

    def initialize_buttons(self):
        btn1 = Button.Button(button_id=1, name="Fold", pos_x=500, pos_y=540)
        btn2 = Button.Button(button_id=2, name="Check", pos_x=640, pos_y=540)
        btn3 = Button.Button(button_id=3, name="Bet", pos_x=780, pos_y=540)

        self.buttonList.append(btn1)
        self.buttonList.append(btn2)
        self.buttonList.append(btn3)

    def initialize_cards(self):
        for player in self.playerList:
            player.set_cards([self.deck.draw_card(), self.deck.draw_card()])
            self.cardList.extend(player.get_cards())
            if player.get_number() == 1:
                player.set_cards_face_up(True)
    # ------------------------

    # ---DEAL COMMUNITY CARDS---
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
    # --------------------------

    # ---HANDLE GAME LOOP---
    def game_loop(self):

        # ---SWITCH TO NEXT PLAYER---
        def next_player():
            self.turn = (self.turn + 1) % len(self.playerList)
            self.current_player.end_turn()
            self.current_player = self.playerList[self.turn]
            self.current_player.start_turn()

            # if self.phase == 1:
            #     if self.turn == self.big_blind:
            #         self.pot.set_min_bet(0)
            #     elif self.turn == self.small_blind:
            #         self.pot.set_min_bet(int(self.pot.min_bet / 2))
            #     else:
            #         self.pot.set_min_bet(self.pot.bet_amount)


            if self.lead_position == self.turn % len(self.playerList):
                self.phase += 1
                for player in self.playerList:
                    player.set_chips_bet_in_round(0)
                if self.phase == 5:
                    self.showdown()
                    return
                print(f"Starting phase {self.phase}")
                self.deal_community_cards(self.phase)
                self.pot.set_min_bet(0)

        # ---REACT TO BUTTON PRESS---
        def do_action(leadPosition, turn, button_pressed):
            index = leadPosition + turn % len(self.playerList)

            action = button_pressed.get_name()

            if action == "Fold":
                print(f"Player {index} folded")
                self.current_player.fold()
                return True
            if action == "Check":
                print(f"Player {index} checked")
                return True
            if action == "Bet":
                print(f"Player {index} bet")
                self.lead_position = turn
                return self.pot.bet(self.current_player)
            if action == "Call":
                print(f"Player {index} called")
                return self.pot.call(self.current_player)
            if action == "Raise":
                print(f"Player {index} raised")
                self.lead_position = turn
                return self.pot.raise_bet(self.current_player)

        button_pressed = self.handle_events()



        if button_pressed is not None:
            if button_pressed.get_name() in ("Fold", "Check", "Bet", "Call", "Raise"):  # Do action and advance to
                # next player
                if do_action(self.lead_position, self.turn, button_pressed):
                    next_player()

        if self.current_player.has_folded():
            next_player()
            return
    # ----------------------

    # ---UPDATE DISPLAY---
    def update(self):
        # Clear the sequence of images that will be updated
        self.objectImagesToUpdateSequence.clear()
        self.objectImagesToUpdateQueue.clear()

        for player in self.playerList:
            self.objectImagesToUpdateQueue.append(player)
        # objectImagesToUpdateQueue.extend(player.getCards())

        for button in self.buttonList:

            def _update_buttons():
                if button.get_name() == "Check":
                    if self.pot.required_to_call > 0:
                        button.change_button("Call")
                if button.get_name() == "Call":
                    if self.pot.required_to_call == 0:
                        button.change_button("Check")
                if button.get_name() == "Bet":
                    if self.pot.required_to_call > 0:
                        button.change_button("Raise")
                if button.get_name() == "Raise":
                    if self.pot.required_to_call == 0:
                        button.change_button("Bet")

            _update_buttons()
            self.objectImagesToUpdateQueue.append(button)

        for card in self.cardList:
            if card.is_moving():
                card.update_position()

            self.objectImagesToUpdateQueue.append(card)

        for text in self.textObjectList:
            self.objectImagesToUpdateQueue.append(text)

        self.objectImagesToUpdateQueue.append(self.deck)
        self.objectImagesToUpdateQueue.append(self.pot.pot_text)
        self.objectImagesToUpdateQueue.append(self.pot.min_bet_text)

        for each in self.objectImagesToUpdateQueue:
            self.objectImagesToUpdateSequence.append((each.get_image(), each.get_rect()))

        self.user_interface.update_display(self.objectImagesToUpdateSequence)
    # --------------------

    def showdown(self):
        print("SHOWDOWN!")
        win_list = [[100, -1, "none"]]

        for player in self.playerList:
            if player.has_folded() is False:
                player.set_cards_face_up(True)
                card_list = player.get_cards()
                card_list.extend(self.communityCards)
                player_score = self.calculate_hand_score(card_list)
                count = 1
                for key, value in player_score.items():
                    if value is True:
                        print(f"Player {player.get_number()} has a {key}.")
                        if win_list[0][0] > count:
                            win_list.clear()
                            win_list.append([count, player, key])
                            break
                        if win_list[0][0] == count:
                            win_list.append([count, player, key])
                            break
                        break
                    count += 1

        for winner in win_list:
            player: Player.Player = winner[1]

            print(f"Player {player.get_number()} wins!")
            player.set_chips(player.get_chips() + int(self.pot.pot/len(win_list)))

        if len(win_list) == 1:
            win_text = Text.Text(f"Player {win_list[0][1].get_number()} wins!", 64, (0, 0, 0), None)
            win_text.move_to(320, 320)
        else:
            win_string = "Players "
            for winner in win_list:
                win_string += f"{winner[1].get_number()}, "
            win_string = win_string[:-2]
            win_string += " split the pot!"
            win_text = Text.Text(win_string, 32, (0, 0, 0), None)
            win_text.move_to(460, 320)

        self.textObjectList.append(win_text)

        clock = pygame.time.Clock()
        self.update()
        clock.tick(60)
        pygame.time.delay(3000)
        self.initialize_game_objects(False)


    def calculate_hand_score(self, card_list: list):

        def pair(a_card_list: list):
            for card in a_card_list:
                for compare_card in a_card_list:
                    if card == compare_card:
                        continue
                    if card.get_value()["number"] == compare_card.get_value()["number"]:
                        return True
            return False

        def two_pair(a_card_list: list):
            pairs = 0
            pair_cards = []  # Cards already made into pairs
            for card in a_card_list:
                for compare_card in a_card_list:
                    if card == compare_card or card in pair_cards or compare_card in pair_cards:
                        continue
                    if card.get_value()["number"] == compare_card.get_value()["number"]:
                        pairs += 1
                        pair_cards.extend([card, compare_card])
                        continue
            if pairs >= 2:
                return True
            return False

        def three_of_a_kind(a_card_list: list):
            for card in a_card_list:
                no_of_card_matches = 1
                i = a_card_list.index(card) + 1
                for compare_card in a_card_list[i:]:
                    if card.get_value()["number"] == compare_card.get_value()["number"]:
                        no_of_card_matches += 1
                        if no_of_card_matches == 3:
                            return True
            return False

        def straight(a_card_list: list):
            a_card_list.sort(key=lambda x: x.get_value()["number"])
            last_number = a_card_list[0].get_value()["number"]
            count = 1
            for card in a_card_list[1:]:
                if card.get_value()["number"] == last_number + 1:
                    count += 1
                    last_number = card.get_value()["number"]
                    if count == 5:
                        return True
                else:
                    count = 1
                    last_number = card.get_value()["number"]
            return False

        if card_list is None:
            print("card_list is empty")
            return

        hand_score = {"royal_flush": False, "straight_flush": False, "four_of_a_kind": False, "full_house": False,
                      "flush": False, "straight": straight(card_list), "three_of_a_kind": three_of_a_kind(card_list), "two_pair": two_pair(card_list),
                      "pair": pair(card_list), "high_card": True}

        return hand_score

    def main(self):
        pygame.init()
        clock = pygame.time.Clock()

        self.user_interface.init_display()
        self.initialize_game_objects()

        while True:
            self.game_loop()
            self.update()
            clock.tick(60)

class Pot:

    def __init__(self):
        self.pot: int = 0
        self.required_to_call: int = 4
        self.bet_amount = self.required_to_call    # Used to hold onto min_bet when it is modified for blinds
        self.raise_amount: int = 8
        self.increment = 4
        self.pot_text = Text.Text("Pot: -1", 32, (0, 0, 0), None)
        self.pot_text.move_to(30, 30)
        self.min_bet_text = Text.Text("Min bet: -1", 32, (0, 0, 0), None)
        self.min_bet_text.move_to(30, 60)
        self.update_text()

    def set_min_bet(self, min_bet: int):
        self.required_to_call = min_bet
        self.update_text()

    def bet_blinds(self, big_blind_player: Player.Player, small_blind_player: Player.Player):
        big_blind_player.set_chips(big_blind_player.get_chips() - self.bet_amount)
        big_blind_player.set_chips_bet_in_round(self.bet_amount)
        small_blind_player.set_chips(small_blind_player.get_chips() - int(self.bet_amount / 2))
        small_blind_player.set_chips_bet_in_round(int(self.bet_amount / 2))
        self.add_to_pot(6)
        pass

    def bet(self, player: Player.Player) -> bool:
        player_chips = player.get_chips()
        bet_amount = self.bet_amount

        if player_chips >= bet_amount:
            player.set_chips(player_chips - bet_amount)
            player.set_chips_bet_in_round(bet_amount)
            self.add_to_pot(bet_amount)
            self.set_min_bet(bet_amount)
            return True
        # else
        return False

    def call(self, player: Player.Player):
        player_chips = player.get_chips()
        player_chips_bet_in_round = player.get_chips_bet_in_round()
        chips_required_to_call = self.required_to_call - player_chips_bet_in_round
        if chips_required_to_call <= player_chips:
            player.set_chips(player_chips - chips_required_to_call)
            player.set_chips_bet_in_round(chips_required_to_call)
            self.add_to_pot(chips_required_to_call)
            return True
        return False

    def raise_bet(self, player: Player.Player):
        player_chips = player.get_chips()
        bet_amount = self.required_to_call + self.increment

        if player_chips >= bet_amount:
            player.set_chips(player_chips - (bet_amount - player.get_chips_bet_in_round()))
            player.set_chips_bet_in_round(bet_amount)
            self.add_to_pot(bet_amount)
            self.set_min_bet(bet_amount)
            return True
        # else
        return False

    def add_to_pot(self, amount):
        self.pot += amount
        self.update_text()

    def update_text(self):
        self.pot_text.set_text(f"Pot: {self.pot}")
        self.min_bet_text.set_text(f"Min bet: {self.required_to_call}")


if __name__ == '__main__':
    game = PokerInPython()
    game.main()
