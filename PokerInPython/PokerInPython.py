import sys
import pygame
import os

import UserInterface
import Card
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
        object_pressed = None

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
                object_pressed = self.user_interface.check_button_presses(self.buttonList)
                if object_pressed is None:  # Check card presses
                    object_pressed = self.user_interface.check_card_presses(self.cardList)

        mouse_pos = pygame.mouse.get_pos()
        self.user_interface.mouse_pos = mouse_pos

        if object_pressed is not None:
            return object_pressed
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

        self.pot.set_min_bet(self.pot.small_bet)

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

        bet_panel = Button.Button(button_id=4, name="Bet_Display", pos_x=669, pos_y=515)
        raise_panel = Button.Button(button_id=4, name="Bet_Display", pos_x=809, pos_y=515)
        self.buttonList.append(bet_panel)
        self.buttonList.append(raise_panel)

        bet_text = Text.Text("4", 26, (0, 0, 0), None)
        bet_text.move_to(680, 517)
        raise_text = Text.Text("8", 26, (0, 0, 0), None)
        raise_text.move_to(820, 517)

        self.textObjectList.append(bet_text)
        self.textObjectList.append(raise_text)
        self.pot.bet_text = bet_text
        self.pot.raise_text = raise_text

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

            if self.current_player.get_number() == 1:
                self.pot.update_call_raise_display(self.current_player.get_chips_bet_in_round(), self.phase)

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
                return self.pot.bet(self.current_player, self.phase)
            if action == "Call":
                print(f"Player {index} called")
                return self.pot.call(self.current_player)
            if action == "Raise":
                print(f"Player {index} raised")
                self.lead_position = turn
                return self.pot.raise_bet(self.current_player, self.phase)

        # Check if player has clicked on an object
        object_pressed = self.handle_events()

        if object_pressed is not None:
            if isinstance(object_pressed, Button.Button):   # If object is a button
                if object_pressed.get_name() in ("Fold", "Check", "Bet", "Call", "Raise"):  # Do action and advance to
                    # next player
                    if do_action(self.lead_position, self.turn, object_pressed):
                        next_player()
            if isinstance(object_pressed, Card.Card):   # If object is a card
                card_pressed = object_pressed
                # Return the new card clicked on by the user
                new_card = self.user_interface.show_card_menu(self.deck)
                # Check if the card being replaced is held by a player
                for player in self.playerList:
                    if card_pressed in player.get_cards():
                        player.change_cards(card_pressed, new_card)
                        self.cardList.remove(card_pressed)
                        self.cardList.append(new_card)
                        self.deck.remove_card(new_card)
                        self.deck.insert_card(card_pressed)
                        return
                # Check if the card being replaced is a community card
                if card_pressed in self.communityCards:
                    self.communityCards.append(new_card)
                    self.communityCards.remove(card_pressed)
                    self.cardList.remove(card_pressed)
                    self.cardList.append(new_card)
                    self.deck.remove_card(new_card)
                    self.deck.insert_card(card_pressed)
                    new_card.move_to(card_pressed.get_rect().x, card_pressed.get_rect().y)
                    return
                print("Couldn't find card")



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

        for each in self.objectImagesToUpdateQueue:
            self.objectImagesToUpdateSequence.append((each.get_image(), each.get_rect()))

        self.user_interface.update_display(self.objectImagesToUpdateSequence)
    # --------------------

    def showdown(self):

        def calculate_hand_score(card_list: list):

            def pair(a_card_list: list):
                a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                for card in a_card_list:
                    for compare_card in a_card_list:
                        if card == compare_card:
                            continue
                        if card.get_value()["number"] == compare_card.get_value()["number"]:
                            a_card_list.remove(card)
                            a_card_list.remove(compare_card)
                            a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                            a_card_list.insert(0, card)
                            a_card_list = a_card_list[:4]
                            return a_card_list
                return []

            def two_pair(a_card_list: list):
                a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
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
                    pair_cards.sort(key=lambda x: x.get_value()["number"], reverse=True)
                    for card in pair_cards:
                        a_card_list.remove(card)
                    a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                    a_card_list.insert(0, pair_cards[0])
                    a_card_list.insert(1, pair_cards[2])
                    return a_card_list[:3]
                return []

            def three_of_a_kind(a_card_list: list):
                a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                match_cards = []
                for card in a_card_list:
                    no_of_card_matches = 1
                    match_cards.clear()
                    i = a_card_list.index(card) + 1
                    for compare_card in a_card_list[i:]:
                        if card.get_value()["number"] == compare_card.get_value()["number"]:
                            no_of_card_matches += 1
                            match_cards.append(compare_card)
                            if no_of_card_matches == 3:
                                match_cards.append(card)
                                for m_card in match_cards:
                                    a_card_list.remove(m_card)
                                a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                                a_card_list.insert(0, card)

                                return a_card_list[:3]
                return []

            def straight(a_card_list: list):
                a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                last_number = a_card_list[0].get_value()["number"]  # The value of the last card compared
                count = 1
                first_card = a_card_list[0]  # The highest card in the straight
                for card in a_card_list[1:]:
                    if card.get_value()["number"] == last_number - 1:
                        count += 1
                        last_number = card.get_value()["number"]
                        if count == 5:
                            return [first_card]
                    else:
                        count = 1
                        last_number = card.get_value()["number"]
                        first_card = card
                return []

            def flush(a_card_list: list):
                a_card_list.sort(key=lambda x: x.get_value()["suit"])
                suit_count = 0
                flush_cards = []
                last_suit = "none"
                for card in a_card_list:
                    if card.get_value()["suit"] == last_suit:
                        suit_count += 1
                        flush_cards.append(card)
                    else:
                        # Don't check suit_count until we have checked all cards of a suit
                        # That way, if we have 6 of a suit, we take the highest 5
                        if suit_count >= 5:
                            flush_cards.sort(key=lambda x: x.get_value()["number"])
                            return flush_cards[:5]
                        flush_cards.clear()
                        suit_count = 1
                        last_suit = card.get_value()["suit"]
                return []

            def full_house(a_card_list: list):
                a_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)

                def check_threes(b_card_list: list):
                    three_cards = []
                    for card in a_card_list:
                        no_of_card_matches = 1
                        three_cards.clear()
                        i = a_card_list.index(card) + 1
                        for compare_card in a_card_list[i:]:
                            if card.get_value()["number"] == compare_card.get_value()["number"]:
                                no_of_card_matches += 1
                                three_cards.append(compare_card)
                                if no_of_card_matches == 3:
                                    three_cards.append(card)
                                    return three_cards
                    return []

                def check_pairs(c_card_list: list):
                    c_card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)
                    for card in a_card_list:
                        next_index = c_card_list.index(card) + 1
                        if next_index >= len(c_card_list):
                            return []
                        next_card = c_card_list[next_index]
                        if card.get_value()["number"] == next_card.get_value()["number"]:
                            return [card, next_card]
                    return []

                threes = check_threes(a_card_list)
                if len(threes) > 0:
                    pairs = check_pairs(a_card_list)
                    if len(pairs) > 0:
                        threes.extend(pairs)
                        return threes
                return []




            if card_list is None:
                print("card_list is empty")
                return

            hand_score = [0, 0, 0, 0, 0, 0]

            def add_rank_to_hand_score(a_kicker_list, rank_value):
                hand_score[0] = rank_value
                for i, card in enumerate(a_kicker_list):
                    hand_score[i+1] = card.get_value()["number"]

            # Check each hand rank
            # If it returns a list of cards, turn it into a hand score
            kicker_list = full_house(card_list)
            if len(kicker_list) > 0:
                add_rank_to_hand_score(kicker_list, 7)
            else:
                kicker_list = flush(card_list)
                if len(kicker_list) > 0:
                    add_rank_to_hand_score(kicker_list, 6)
                else:
                    kicker_list = straight(card_list)
                    if len(kicker_list) > 0:
                        add_rank_to_hand_score(kicker_list, 5)
                    else:
                        kicker_list = three_of_a_kind(card_list)
                        if len(kicker_list) > 0:
                            add_rank_to_hand_score(kicker_list, 4)
                        else:
                            # two pair
                            kicker_list = two_pair(card_list)
                            if len(kicker_list) > 0:
                                add_rank_to_hand_score(kicker_list, 3)
                            else:
                                # pair
                                kicker_list = pair(card_list)
                                if len(kicker_list) > 0:
                                    add_rank_to_hand_score(kicker_list, 2)

            return hand_score


        def compare_hands(a_player_score, a_win_score):
            for i in range(0, len(a_player_score)):
                if a_player_score[i] > a_win_score[i]:
                    return 1
                if a_player_score[i] < a_win_score[i]:
                    return -1
            return 0

        # A list of the winning players, with their hand score
        win_list = [[self.playerList[0], [0, 0, 0, 0, 0, 0]]]

        # Determine each players hand
        for player in self.playerList:
            if player.has_folded() is False:
                player.set_cards_face_up(True)
                card_list = player.get_cards()
                card_list.extend(self.communityCards)
                player_score = calculate_hand_score(card_list)

                # Compare players hand to current winning hand
                # is_better > 0 means it beats, == 0 means it ties
                is_better = compare_hands(player_score, win_list[0][1])
                if is_better > 0:
                    win_list.clear()
                    win_list = [[player, player_score]]
                if is_better == 0:
                    win_list.append([player, player_score])

        for winner in win_list:
            player = winner[0]

            print(f"Player {player.get_number()} wins with {winner[1][0]}!")
            player.set_chips(player.get_chips() + int(self.pot.pot/len(win_list)))


        if len(win_list) == 1:
            win_text = Text.Text(f"Player {win_list[0][0].get_number()} wins!", 64, (0, 0, 0), None)
            win_text.move_to(320, 320)
        else:
            win_string = "Players "
            for winner in win_list:
                win_string += f"{winner[0].get_number()}, "
            win_string = win_string[:-2]
            win_string += " split the pot!"
            win_text = Text.Text(win_string, 32, (0, 0, 0), None)
            win_text.move_to(460, 320)

        self.textObjectList.append(win_text)

        clock = pygame.time.Clock()
        self.update()
        clock.tick(60)
        pygame.time.delay(3000)

        for i in range(0, 10):
            continue

        pygame.event.get()
        while pygame.mouse.get_pressed()[0] == 0:
            pygame.event.get()


        self.initialize_game_objects(False)




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
        self.small_bet: int = 4
        self.big_bet: int = 8
        self.required_to_call = 0
        self.pot_text = Text.Text("Pot: -1", 32, (0, 0, 0), None)
        self.pot_text.move_to(30, 30)

        self.bet_text = Text.Text("none", 32, (0, 0, 0), None)
        self.raise_text = Text.Text("none", 32, (0, 0, 0), None)

        self.update_text()


    def set_min_bet(self, min_bet: int):
        self.required_to_call = min_bet
        self.update_text()

    def bet_blinds(self, big_blind_player: Player.Player, small_blind_player: Player.Player):
        big_blind_player.set_chips(big_blind_player.get_chips() - self.small_bet)
        big_blind_player.set_chips_bet_in_round(self.small_bet)
        small_blind_player.set_chips(small_blind_player.get_chips() - int(self.small_bet / 2))
        small_blind_player.set_chips_bet_in_round(int(self.small_bet / 2))
        self.add_to_pot(6)
        pass

    def bet(self, player: Player.Player, phase: int) -> bool:
        player_chips = player.get_chips()
        if phase in (0, 1, 2):
            bet_amount = self.small_bet
        else:
            bet_amount = self.big_bet

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
            player.set_chips_bet_in_round(chips_required_to_call + player.get_chips_bet_in_round())
            self.add_to_pot(chips_required_to_call)
            return True
        return False

    def raise_bet(self, player: Player.Player, phase: int):
        player_chips = player.get_chips()

        if phase in (0, 1, 2):
            bet_amount = self.required_to_call + self.small_bet
        else:
            bet_amount = self.required_to_call + self.big_bet

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

    def update_call_raise_display(self, amount_already_bet: int, phase: int):
        self.bet_text.set_text(f"{self.required_to_call - amount_already_bet}")
        if phase in (0, 1):
            self.raise_text.set_text(f"{self.small_bet + self.required_to_call - amount_already_bet}")
        else:
            self.raise_text.set_text(f"{self.big_bet + self.required_to_call - amount_already_bet}")


if __name__ == '__main__':
    game = PokerInPython()
    game.main()
