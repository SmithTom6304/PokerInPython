import sys
import pygame
import os

import UserInterface
import Card
import Player
import Deck
import Button
import Text

import time
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 35)


def calculate_hand_score(card_list: list):
    """
    Determine the value of a hand.
    e.g. Pair with a 7 kicker, straight flush

    :param card_list: List of cards to be ranked. Players hole cards and the community cards

    :return: List of ints [0, 0, 0, 0, 0, 0]. First value is the rank (0 = high card, 1 = pair etc.)
    Remaining values are for the value of the card rank and the value of the kickers.


    For example:

    Three-of-a-kind sixes with a king and a 10 as kicker would return [4, 6, 13, 10, 0, 0].

    Ace high-card with 10, 8, 6, 4 kickers would return [1, 14, 10, 8, 6, 4]

    """
    def high_card(a_card_list: list):
        return a_card_list[:5]

    def pair(a_card_list: list):
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
        last_number = a_card_list[0].get_value()["number"]  # The value of the last card compared
        count = 1
        first_card = a_card_list[0]  # The highest card in the straight
        for card in a_card_list[1:]:
            if card.get_value()["number"] == last_number - 1:
                count += 1
                last_number = card.get_value()["number"]
                if last_number == 2 and a_card_list[0].get_value()["number"] == 14:
                    count += 1
                if count == 5:
                    return [first_card]
            elif card.get_value()["number"] == last_number:
                continue
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
                flush_cards.append(card)
                suit_count = 1
                last_suit = card.get_value()["suit"]
        if suit_count >= 5:
            flush_cards.sort(key=lambda x: x.get_value()["number"])
            return flush_cards[:5]
        return []

    def full_house(a_card_list: list):

        def check_threes(b_card_list: list):
            three_cards = []
            for card in a_card_list:
                no_of_card_matches = 1
                three_cards.clear()
                i = b_card_list.index(card) + 1
                for compare_card in a_card_list[i:]:
                    if card.get_value()["number"] == compare_card.get_value()["number"]:
                        no_of_card_matches += 1
                        three_cards.append(compare_card)
                        if no_of_card_matches == 3:
                            three_cards.append(card)
                            return three_cards
            return []

        def check_pairs(c_card_list: list):
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
            # Remove card from a_card_list if card in threes
            a_card_list = [x for x in a_card_list if x not in threes]
            pairs = check_pairs(a_card_list)
            if len(pairs) > 0:
                threes.extend(pairs)
                return threes
        return []

    def four_of_a_kind(a_card_list: list):
        four_cards = []
        for card in a_card_list:
            no_of_card_matches = 1
            four_cards.clear()
            i = a_card_list.index(card) + 1
            for compare_card in a_card_list[i:]:
                if card.get_value()["number"] == compare_card.get_value()["number"]:
                    no_of_card_matches += 1
                    four_cards.append(compare_card)
                    if no_of_card_matches == 4:
                        four_cards.append(card)
                        # Remove card from a_card_list if card in four_cards
                        a_card_list = [x for x in a_card_list if x not in four_cards]
                        a_card_list.insert(0, card)
                        return a_card_list[:2]
                        # return four_cards
        return []

    def straight_flush(a_card_list: list):
        a_card_list.sort(key=lambda x: (x.get_value()["suit"], x.get_value()["number"]), reverse=True)
        split_list = [[], [], [], []]

        for card in a_card_list:
            if card.get_value()["suit"] == 'D':
                split_list[0].append(card)
            if card.get_value()["suit"] == 'C':
                split_list[1].append(card)
            if card.get_value()["suit"] == 'H':
                split_list[2].append(card)
            if card.get_value()["suit"] == 'S':
                split_list[3].append(card)

        a_kicker_list = []
        for a_list in split_list:
            if len(a_list) == 0:
                continue
            a_kicker_list = straight(a_list)
            if len(a_kicker_list) > 0:
                return a_kicker_list
        return a_kicker_list

    def royal_flush(a_card_list: list):
        a_card_list.sort(key=lambda x: (x.get_value()["suit"]), reverse=True)
        last_number = a_card_list[0].get_value()["number"]  # The value of the last card compared
        count = 1
        first_card = a_card_list[0]  # The highest card in the straight
        last_suit = first_card.get_value()["suit"]
        for card in a_card_list[1:]:
            if first_card.get_value()["number"] != 14:
                first_card = card
                last_suit = card.get_value()["suit"]
                last_number = card.get_value()["number"]
                count = 1
                continue
            if card.get_value()["suit"] == last_suit:
                if card.get_value()["number"] == last_number - 1:
                    count += 1
                    last_number = card.get_value()["number"]
                    if count == 5:
                        return [first_card]
                else:
                    count = 1
                    last_number = card.get_value()["number"]
                    first_card = card
            else:
                last_suit = card.get_value()["suit"]
                last_number = card.get_value()["number"]
                count = 1
        return []

    if card_list is None:
        print("card_list is empty")
        return

    hand_score = [0, 0, 0, 0, 0, 0]

    def add_rank_to_hand_score(a_kicker_list, rank_value):
        hand_score[0] = rank_value
        for i, card in enumerate(a_kicker_list):
            hand_score[i + 1] = card.get_value()["number"]

    # Check each hand rank
    # If it returns a list of cards, turn it into a hand score

    card_list.sort(key=lambda x: x.get_value()["number"], reverse=True)

    kicker_list = royal_flush(card_list.copy())
    if len(kicker_list) > 0:
        add_rank_to_hand_score(kicker_list, 10)
    else:
        kicker_list = straight_flush(card_list.copy())
        if len(kicker_list) > 0:
            add_rank_to_hand_score(kicker_list, 9)
        else:
            kicker_list = four_of_a_kind(card_list.copy())
            if len(kicker_list) > 0:
                add_rank_to_hand_score(kicker_list, 8)
            else:
                kicker_list = full_house(card_list.copy())
                if len(kicker_list) > 0:
                    add_rank_to_hand_score(kicker_list, 7)
                else:
                    kicker_list = flush(card_list.copy())
                    if len(kicker_list) > 0:
                        add_rank_to_hand_score(kicker_list, 6)
                    else:
                        kicker_list = straight(card_list.copy())
                        if len(kicker_list) > 0:
                            add_rank_to_hand_score(kicker_list, 5)
                        else:
                            kicker_list = three_of_a_kind(card_list.copy())
                            if len(kicker_list) > 0:
                                add_rank_to_hand_score(kicker_list, 4)
                            else:
                                # two pair
                                kicker_list = two_pair(card_list.copy())
                                if len(kicker_list) > 0:
                                    add_rank_to_hand_score(kicker_list, 3)
                                else:
                                    # pair
                                    kicker_list = pair(card_list.copy())
                                    if len(kicker_list) > 0:
                                        add_rank_to_hand_score(kicker_list, 2)
                                    else:
                                        kicker_list = high_card(card_list.copy())
                                        add_rank_to_hand_score(kicker_list, 1)

    return hand_score


def compare_hands(a_player_score: list, a_win_score: list) -> int:
    """
    Compare two hand scores, and determine which one is better.

    :param a_player_score: First hand score to be compared
    :param a_win_score: Hand score to be compared with.

    :return: 1 if a_player_score is better, -1 if a_win_score is better, 0 if they are equal

    """
    for i in range(0, len(a_player_score)):
        if a_player_score[i] > a_win_score[i]:
            return 1
        if a_player_score[i] < a_win_score[i]:
            return -1
    return 0


def simulate_games(hole_cards: list, current_community_cards: list, no_of_players: int, simulations=1000) -> float:
    """
    Simulate a number of games, to determine how likely a hand is to win the round.

    :param hole_cards: Players two hole cards
    :param current_community_cards: The community cards that have been dealt so far
    :param no_of_players: The players remaining in the round
    :param simulations: Number of games to be simulated. A higher number will increase accuracy, but take longer

    :return: Estimated chance to win the round. A float between 0.0 and 1.0

    """
    # Code modified from http://cowboyprogramming.com/2007/01/04/programming-poker-ai/
    score = 0.0
    won_games = 0
    sim_deck = Deck.Deck()
    copy_deck = Deck.Deck()
    sim_deck.remove_cards_by_val(hole_cards)
    sim_deck.remove_cards_by_val(current_community_cards)
    sim_deck.shuffle_deck()

    start_time = time.time()
    for _unused_i in range(0, simulations):

        copy_deck.deck = sim_deck.deck.copy()
        copy_deck.shuffle_deck()
        players = [hole_cards]
        scores = []
        win_score = [0, 0, 0, 0, 0, 0]
        winners = 1
        community_cards = current_community_cards.copy()

        for _unused_j in range(1, no_of_players):
            players.append([copy_deck.draw_card(), copy_deck.draw_card()])
        while len(community_cards) < 5:
            community_cards.append(copy_deck.draw_card())

        for player_hand in players:
            card_list = player_hand.copy()
            card_list.extend(community_cards)
            player_score = calculate_hand_score(card_list)
            scores.append(player_score)
            is_better = compare_hands(player_score, win_score)
            if is_better > 0:
                win_score = player_score
                winners = 1
            if is_better == 0:
                winners += 1

        if scores[0] == win_score:
            score += 1/winners
            won_games += 1





    end_time = time.time()
    delta_t = end_time - start_time

    print(f"Simulation took {round(delta_t, 3)}s")
    print(f"Simulation scored {round(score/simulations, 3)}, with {won_games} games won")

    # score = random.random()
    return score/simulations


class PokerInPython:

    # Queue of objects to be added to the sequence to update
    draw_queue = []
    # List of (image, rect) tuples to provide to UserInterface layer to update screen
    draw_sequence = [None, None]

    # Lists of game objects
    player_list = []
    button_list = []
    card_list = []
    text_object_list = []
    community_cards = []  # Sublist of card_list

    # To draw an object, we can either add the object to the update queue
    # or we can add it to the relevant list
    # The update function handles providing the objects to the UserInterface module

    DEV_MODE = True


    def __init__(self):
        self.pot = Pot()
        self.deck = Deck.Deck()
        self.user_interface = UserInterface.UserInterface()
        self.user_interface.change_background("UI")
        self.exit = False

        self.start_lead_position = 0    # Index of first player in round. Effectively the dealer.
        self.lead_position = 0  # Index of the current leading player, or player who raised last
        self.turn = 0   # Index of the player who is currently taking their turn

        self.phase = 1  # https://www.poker-king.com/dictionary/community_cards/
        # Phase 1 - Deal private cards, then bet
        # Phase 2 - Deal three community cards to form the flop, then bet
        # Phase 3 - Deal fourth community card, called the turn, then bet
        # Phase 4 - Deal last community card, called the river, then bet
        # Showdown - show cards

        self.raises_in_round = 0    # Number of times player has raised in this round. Max 3

        self.current_player: Player.Player = None

        self.btn_click_sound = pygame.mixer.Sound("./Sounds/btn_click.wav")

    # ---INPUT HANDLING---
    def handle_events(self):
        """Handle input events

        :return: Object pressed
        """
        object_pressed = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.DEV_MODE is True:
                    self.initialize_game_objects()
                if event.key == pygame.K_RIGHT and self.DEV_MODE is True:
                    for card in self.card_list:
                        card.set_face_up(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for object presses
                object_pressed = self.user_interface.check_button_presses(self.button_list)
                if object_pressed is None:  # Check card presses
                    object_pressed = self.user_interface.check_card_presses(self.card_list)

        if object_pressed is not None:
            return object_pressed

    # ---INITIALIZATION---
    def initialize_game_objects(self, initialize_players=True):
        if initialize_players is True:
            self.player_list.clear()
            self.initialize_players(number_of_players=4, chips=100)

        self.deck.move_deck(220, 390)

        self.button_list.clear()
        self.card_list.clear()
        self.text_object_list.clear()
        self.community_cards.clear()
        self.deck.reset_deck()
        self.pot.reset()

        self.phase = 1

        # Reset players
        for player in self.player_list:
            player.reset()
            self.text_object_list.append(player.get_text())

        self.round_initialization()
        self.initialize_cards()
        self.initialize_buttons()

        # Add wait frames to each card to create ripple effect
        for i, card in enumerate(self.card_list):
            card.set_wait_frames((len(self.card_list) - i) * 3)

    def round_initialization(self):

        def determine_players_left_in_round():
            a_players_left_in_game = len(self.player_list)
            for player in self.player_list:
                if player.get_chips() <= 0:
                    player.set_has_lost(True)
                    a_players_left_in_game -= 1
            return a_players_left_in_game

        def determine_blind_indexes() -> [int, int]:
            big_blind = self.lead_position - 1
            small_blind = self.lead_position - 2
            blinds_selected = False
            while not blinds_selected:
                if big_blind < 0:
                    big_blind += len(self.player_list)
                if small_blind < 0:
                    small_blind += len(self.player_list)

                if self.player_list[big_blind].has_lost():
                    big_blind -= 1
                    small_blind -= 1
                    continue
                if self.player_list[big_blind].get_chips() < self.pot.small_bet:
                    self.player_list[big_blind].set_has_lost(True)
                    big_blind -= 1
                    small_blind -= 1
                    continue
                if self.player_list[small_blind].has_lost():
                    small_blind -= 1
                    continue
                if self.player_list[small_blind].get_chips() < int(self.pot.small_bet / 2):
                    self.player_list[small_blind].set_has_lost(True)
                    small_blind -= 1
                    continue

                blinds_selected = True

            return [big_blind, small_blind]

        self.lead_position = self.start_lead_position
        self.start_lead_position = (self.start_lead_position + 1) % len(self.player_list)
        self.turn = self.lead_position
        self.current_player = self.player_list[self.lead_position]
        self.current_player.start_turn()

        _unused_players_left_in_game = determine_players_left_in_round()

        blind_indexes = determine_blind_indexes()

        self.pot.bet_blinds(self.player_list[blind_indexes[0]], self.player_list[blind_indexes[1]])
        self.pot.set_min_bet(self.pot.small_bet)

    def initialize_players(self, number_of_players, chips):
        player1 = Player.Player(1, chips, confidence=100, pos_x=47, pos_y=355)
        self.player_list.append(player1)

        for i in range(2, number_of_players + 1):
            x_value = 100 + (260 * (i - 2))
            player = Player.Player(i, chips, confidence=100, pos_x=x_value, pos_y=(self.user_interface.height / 6))
            self.player_list.append(player)

        self.current_player = self.player_list[0]

    def initialize_buttons(self):
        btn1 = Button.Button(button_id=1, name="Fold", pos_x=283, pos_y=540)
        btn2 = Button.Button(button_id=2, name="Check", pos_x=423, pos_y=540)
        btn3 = Button.Button(button_id=3, name="Bet", pos_x=563, pos_y=540)

        self.button_list.append(btn1)
        self.button_list.append(btn2)
        self.button_list.append(btn3)

        bet_panel = Button.Button(button_id=4, name="Bet_Display", pos_x=452, pos_y=515)
        raise_panel = Button.Button(button_id=4, name="Bet_Display", pos_x=593, pos_y=515)
        self.button_list.append(bet_panel)
        self.button_list.append(raise_panel)

        home_btn = Button.Button(button_id=6, name="Home", pos_x=8, pos_y=8)
        music_btn = Button.Button(button_id=7, name="Music", pos_x=800, pos_y=8)

        self.button_list.append(home_btn)
        self.button_list.append(music_btn)

        p1: Player.Player = self.player_list[0]
        player_bet = str(self.pot.small_bet - p1.get_chips_bet_in_round())
        player_raise = str(self.pot.big_bet - p1.get_chips_bet_in_round())
        bet_text = Text.Text(player_bet, 26, (0, 0, 0), None)
        bet_text.move_to(bet_panel.get_rect().x + 11, bet_panel.get_rect().y + 2)
        raise_text = Text.Text(player_raise, 26, (0, 0, 0), None)
        raise_text.move_to(raise_panel.get_rect().x + 11, raise_panel.get_rect().y + 2)

        self.text_object_list.append(bet_text)
        self.text_object_list.append(raise_text)
        self.pot.bet_text = bet_text
        self.pot.raise_text = raise_text

    def initialize_cards(self):
        for player in self.player_list:
            if player.has_lost():
                player.fold(has_cards=False)
                continue
            player.set_cards([self.deck.draw_card(), self.deck.draw_card()])
            self.card_list.extend(player.get_cards())
            if player.get_number() == 1:
                player.set_cards_face_up(True)

    # ---DEAL COMMUNITY CARDS---
    def deal_community_cards(self, phase):
        if phase == 1:
            return
        if phase == 2:
            for i in range(0, 3):
                card = self.deck.draw_card()
                card.set_wait_frames(i * 3)
                card.move(250 + (75 * (i+1)), 390)
                card.set_face_up(True)
                self.community_cards.append(card)
                self.card_list.append(card)
        if phase == 3:
            card = self.deck.draw_card()
            card.move(250 + (75 * (3 + 1)), 390)
            card.set_face_up(True)
            self.community_cards.append(card)
            self.card_list.append(card)
        if phase == 4:
            card = self.deck.draw_card()
            card.move(250 + (75 * (4 + 1)), 390)
            card.set_face_up(True)
            self.community_cards.append(card)
            self.card_list.append(card)

    # ---HANDLE GAME LOOP---
    def game_loop(self):

        # ---SWITCH TO NEXT PLAYER---
        def next_player():
            self.turn = (self.turn + 1) % len(self.player_list)
            self.current_player.end_turn()
            self.current_player = self.player_list[self.turn]
            self.current_player.start_turn()

            if self.current_player.get_number() == 1:
                self.pot.update_call_raise_display(self.current_player.get_chips_bet_in_round(), self.phase)

            if self.lead_position == self.turn % len(self.player_list):
                self.phase += 1
                self.raises_in_round = 0
                for a_player in self.player_list:
                    a_player.set_chips_bet_in_round(0)
                if self.phase == 5:
                    self.showdown()
                    return
                self.deal_community_cards(self.phase)
                self.pot.set_min_bet(0)

        # ---REACT TO BUTTON PRESS---
        def do_action(turn, action):

            if self.current_player.get_number() != 1:
                action_text = Text.Text(action, 24, (0, 0, 0), None)
                action_text.set_timer(1)
                action_text.move_to(self.current_player.get_rect().x + 120, self.current_player.get_rect().y + 30)
                self.text_object_list.append(action_text)
            else:
                if pygame.mixer.music.get_busy():
                    self.btn_click_sound.play()


            if action == "Fold":
                self.current_player.fold()
                return True
            if action == "Check":
                return self.pot.call(self.current_player)
            if action == "Bet":
                self.lead_position = turn
                return self.pot.bet(self.current_player, self.phase)
            if action == "Call":
                return self.pot.call(self.current_player)
            if action == "Raise":
                if self.raises_in_round == 3:
                    return self.pot.call(self.current_player)
                self.lead_position = turn
                self.raises_in_round += 1
                return self.pot.bet(self.current_player, self.phase)
            if action == "Home":
                self.exit = True
            if action == "Music":
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play()

        # Wait until all cards are dealt before allowing actions
        for card in self.card_list:
            if card.is_moving():
                return

        if self.current_player.has_folded():
            next_player()
            return

        # Determine wins by out-betting
        players_left = len(self.player_list)
        player_left = None
        for player in self.player_list:
            if player.has_folded():
                players_left -= 1
            else:
                player_left = player
        if players_left == 1:
            self.showdown(early_winner=player_left)
            return

        # AI ACTION
        if self.current_player.get_number() != 1:
            # Code taken from http://cowboyprogramming.com/2007/01/04/programming-poker-ai/
            players_folded = 0
            for player in self.player_list:
                if player.has_folded():
                    players_folded += 1

            i_players_left = 4 - players_folded

            score = simulate_games(self.current_player.cards.copy(), self.community_cards.copy(),
                                        i_players_left)

            req = self.pot.required_to_call - self.current_player.get_chips_bet_in_round()
            rate_of_return = score * i_players_left

            if i_players_left == 2:
                phase = self.phase
                min_bet = 0
                for i in range(phase, 5):
                    if i in (1, 2):
                        min_bet += self.pot.small_bet
                    if i in (3, 4):
                        min_bet += self.pot.big_bet

                pot_odds = min_bet / (self.pot.pot + min_bet*2)
                rate_of_return = score/pot_odds
                print(f"TWO LEFT: Player{self.current_player.get_number()}ROR = "
                      f"{score}/{pot_odds} = {rate_of_return}")

                # Players should only call when score is bad but RoR
                if score < 0.45 and rate_of_return > 1:
                    print(f"TWO LEFT: Player{self.current_player.get_number()} is hanging on")
                    rate_of_return = 1.05


            delay = random.uniform(0.5, 3)
            # delay = 1
            t_start = time.time()
            clock = pygame.time.Clock()
            while time.time() < t_start + delay:
                self.update()
                clock.tick(60)

            # AI will try to stay in hands with a rate of return greater than 1
            # rand_number will make the AI bluff occasionally on bad hands
            action = ""
            rand_number = random.random()
            if rate_of_return < 0.8:
                if rand_number >= 0.95:
                    action = "Raise"
                else:
                    action = "Fold"
            elif rate_of_return < 1.0:
                if rand_number >= 0.85:
                    action = "Raise"
                elif rand_number >= 0.8:
                    action = "Call"
                else:
                    action = "Fold"
            elif rate_of_return < 1.1:
                if rand_number >= 0.95:
                    action = "Raise"
                else:
                    action = "Call"
            elif rate_of_return < 1.3:
                if rand_number >= 0.6:
                    action = "Raise"
                else:
                    action = "Call"
            else:
                if rand_number > 0.3:
                    action = "Raise"
                else:
                    action = "Call"

            if req == 0 and action == "Fold":
                action = "Check"
            if req == 0 and action == "Call":
                action = "Check"
            if req == 0 and action == "Raise":
                action = "Bet"
            if self.raises_in_round == 3 and action == "Raise":
                action = "Call"
            if req == 0 and self.current_player.get_chips() == 0:
                action = "Check"
            if self.current_player.get_chips() < req:
                action = "Fold"

            if do_action(self.turn, action):
                next_player()


            '''
            if score > 0.7:
                if do_action(self.lead_position, self.turn, "Raise"):
                    next_player()
            elif score > 0.3:
                if do_action(self.lead_position, self.turn, "Call"):
                    next_player()
            else:
                if do_action(self.lead_position, self.turn, "Fold"):
                    next_player()
            '''
        # PLAYER ACTION
        # Check if player has clicked on an object
        object_pressed = self.handle_events()

        if object_pressed is not None:
            if isinstance(object_pressed, Button.Button):   # If object is a button
                if object_pressed.get_name() in ("Fold", "Check", "Bet", "Call", "Raise"):
                    # Do action and advance to next player
                    if do_action(self.turn, object_pressed.get_name()):
                        next_player()
                if object_pressed.get_name() in ("Home", "Music"):
                    do_action(self.turn, object_pressed.get_name())
            if isinstance(object_pressed, Card.Card):   # If object is a card
                card_pressed = object_pressed
                # Return the new card clicked on by the user
                new_card = self.user_interface.show_card_menu(self.deck)
                # Check if the card being replaced is held by a player
                for player in self.player_list:
                    if card_pressed in player.get_cards():
                        player.change_cards(card_pressed, new_card)
                        self.card_list.remove(card_pressed)
                        self.card_list.append(new_card)
                        self.deck.remove_card(new_card)
                        self.deck.insert_card(card_pressed)
                        return
                # Check if the card being replaced is a community card
                if card_pressed in self.community_cards:
                    self.community_cards.append(new_card)
                    self.community_cards.remove(card_pressed)
                    self.card_list.remove(card_pressed)
                    self.card_list.append(new_card)
                    self.deck.remove_card(new_card)
                    self.deck.insert_card(card_pressed)
                    new_card.move_to(card_pressed.get_rect().x, card_pressed.get_rect().y)
                    return
                print("Couldn't find card")

    # ---UPDATE DISPLAY---
    def update(self):

        # Clear the sequence of images that will be updated
        self.draw_sequence.clear()
        self.draw_queue.clear()

        for player in self.player_list:
            self.draw_queue.append(player)
        # objectImagesToUpdateQueue.extend(player.getCards())

        for button in self.button_list:

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
            self.draw_queue.append(button)

        for card in self.card_list:
            if card.is_moving():
                card.update_position()

            self.draw_queue.append(card)

        for text in self.text_object_list:
            if text.check_timer():
                self.text_object_list.remove(text)
                continue
            self.draw_queue.append(text)

        self.draw_queue.append(self.deck)
        self.draw_queue.append(self.pot.pot_text)

        for each in self.draw_queue:
            self.draw_sequence.append((each.get_image(), each.get_rect()))

        self.user_interface.update_display(self.draw_sequence)

    # ---HANDLE END GAME SHOWDOWN---
    def showdown(self, early_winner=None):

        if early_winner is None:

            # A list of the winning players, with their hand score
            win_list = [[self.player_list[0], [0, 0, 0, 0, 0, 0]]]

            # Determine each players hand
            for player in self.player_list:
                if player.has_folded() is False:
                    player.set_cards_face_up(True)
                    card_list = player.get_cards()
                    card_list.extend(self.community_cards)
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

            win_rank = win_list[0][1][0]    # This looks worse than it is.
            win_rank_dict = {10: "ROYAL FLUSH!!!", 9: "Straight Flush!", 8: "Four of a Kind!", 7: "Full House!", 6: "Flush!",
                             5: "Straight!", 4: "Three of a Kind!", 3: "Two Pair!", 2: "Pair!", 1: "High Card!"}
            win_rank_text = win_rank_dict[win_rank]

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

            win_subtext = Text.Text(f"{win_rank_text}", 48, (0, 0, 0), None)
            win_subtext.move_to(460, 440)

            self.text_object_list.append(win_text)
            self.text_object_list.append(win_subtext)

        else:
            win_text = Text.Text(f"Player {early_winner.get_number()} wins!", 64, (0, 0, 0), None)
            early_winner.set_chips(early_winner.get_chips() + int(self.pot.pot))
            win_text.move_to(320, 320)
            self.text_object_list.append(win_text)

        clock = pygame.time.Clock()
        self.update()
        clock.tick(60)
        t1 = time.time()
        t2 = time.time()
        while t2 - t1 < 1.0:
            t2 = time.time()

        pygame.event.get()
        while pygame.mouse.get_pressed()[0] == 0:
            pygame.event.get()

        self.initialize_game_objects(False)

    def main(self):

        def clock_tick():
            clock.tick(60)
            
        pygame.init()
        clock = pygame.time.Clock()

        self.user_interface.init_display()
        self.initialize_game_objects()

        while True:
            self.game_loop()
            self.update()
            if self.exit is True:
                self.exit = False
                break
            clock_tick()


class Pot:

    def __init__(self):
        self.pot: int = 0
        self.small_bet: int = 2
        self.big_bet: int = 4
        self.required_to_call = 0
        self.pot_text = Text.Text("Pot: -1", 32, (0, 0, 0), None)
        self.pot_text.move_to(756, 417)

        self.bet_text = Text.Text("none", 32, (0, 0, 0), None)
        self.raise_text = Text.Text("none", 32, (0, 0, 0), None)

        self.update_text()

    def reset(self):
        self.pot = 0
        self.required_to_call = 0


    def set_min_bet(self, min_bet: int):
        self.required_to_call = min_bet
        self.update_text()

    def bet_blinds(self, big_blind_player: Player.Player, small_blind_player: Player.Player):
        big_blind_player.set_chips(big_blind_player.get_chips() - self.small_bet)
        big_blind_player.set_chips_bet_in_round(self.small_bet)
        small_blind_player.set_chips(small_blind_player.get_chips() - int(self.small_bet / 2))
        small_blind_player.set_chips_bet_in_round(int(self.small_bet / 2))
        self.add_to_pot(int(self.small_bet + (self.small_bet / 2)))
        pass

    def bet(self, player: Player.Player, phase: int) -> bool:
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


class GameHandler:

    def __init__(self):
        self.state = "Menu"
        self.ui = UserInterface.UserInterface()
        self.ui.change_background("Menu")

        self.btn_list = []

    def enter_menu_state(self):
        self.state = "Menu"

        self.btn_list.clear()
        btn1 = Button.Button(0, "Play", 150, 260)
        btn2 = Button.Button(1, "Exit", 395, 253)
        self.btn_list.extend([btn2, btn1])

    def menu(self):

        def check_button_presses():
            button_pressed: Button.Button = self.ui.check_button_presses(self.btn_list)
            if button_pressed is not None:
                action = button_pressed.get_name()
                return action
            return "None"

        def update():
            draw_queue = []
            draw_sequence = []

            for button in self.btn_list:
                draw_queue.append(button)

            for item in draw_queue:
                draw_sequence.append((item.get_image(), item.get_rect()))

            self.ui.update_display(draw_sequence)

        action: str = "None"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                action: str = check_button_presses()

        if action == "Play":
            self.exit_menu_state()
            self.enter_game_state()
        if action == "Exit":
            self.state = "Exit"
            self.exit_menu_state()
        if action == "None":
            update()
        return

    def exit_menu_state(self):
        self.btn_list.clear()

    def enter_game_state(self):
        self.state = "Game"

    def game(self):
        a_game = PokerInPython()
        a_game.main()
        self.exit_game_state()

    def exit_game_state(self):
        self.enter_menu_state()


    def handler(self):

        def clock_tick():
            clock.tick(60)

        pygame.init()
        clock = pygame.time.Clock()
        self.ui.init_display()

        pygame.mixer.init()
        pygame.mixer.music.load("./Sounds/bensound-jazzyfrenchy.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.enter_menu_state()
        while True:


            if self.state == "Menu":
                self.menu()
            if self.state == "Game":
                self.game()
            if self.state == "Exit":
                sys.exit()
            clock_tick()




if __name__ == '__main__':
    # game = PokerInPython()
    # game.main()
    game = GameHandler()
    game.handler()
