import sys
import pygame
import os

import UserInterface
# import Card
import Player
import Deck
import Button

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 35)

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

deck = Deck.Deck()
user_interface = UserInterface.UserInterface()


def handle_events():
    mouse_pos = pygame.mouse.get_pos()
    user_interface.mouse_pos = mouse_pos

    # Clear the sequence of images that will be updated
    objectImagesToUpdateSequence.clear()
    objectImagesToUpdateQueue.clear()

    # objectImagesToUpdateQueue.append(player2)
    # objectImagesToUpdateQueue.append(player3)
    # objectImagesToUpdateQueue.extend(player2.getCards())
    # objectImagesToUpdateQueue.extend(player3.getCards())

    for player in playerList:
        objectImagesToUpdateQueue.append(player)
    # objectImagesToUpdateQueue.extend(player.getCards())

    for button in buttonList:
        objectImagesToUpdateQueue.append(button)

    for card in cardList:
        if card.is_moving():
            card.move_step()

        objectImagesToUpdateQueue.append(card)

    objectImagesToUpdateQueue.append(deck)

    for each in objectImagesToUpdateQueue:
        objectImagesToUpdateSequence.append((each.get_image(), each.get_rect()))

    user_interface.update_display(objectImagesToUpdateSequence)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                initialize_game_objects()
            if event.key == pygame.K_RIGHT:
                for each in cardList:
                    each.set_face_up(True)


def initialize_game_objects():
    playerList.clear()
    buttonList.clear()
    cardList.clear()
    deck.reset_deck()

    initialize_players(4, 100)
    initialize_buttons()
    initialize_cards()

    # Add wait frames to each card to create ripple effect
    for i, card in enumerate(cardList):
        card.set_wait_frames((len(cardList) - i) * 3)


def initialize_players(number_of_players, chips):
    player1 = Player.Player(1, chips, confidence=100, pos_x=80, pos_y=400)
    player1.set_cards([deck.draw_card(), deck.draw_card()])
    player1.set_cards_face_up(True)
    playerList.append(player1)
    cardList.extend(player1.get_cards())

    for i in range(2, number_of_players + 1):
        x_value = (width / number_of_players) * (i - 1)
        player = Player.Player(i, chips, confidence=100, pos_x=x_value, pos_y=(height / 6))
        player.set_cards([deck.draw_card(), deck.draw_card()])
        playerList.append(player)
        cardList.extend(player.get_cards())


def initialize_buttons():
    btn1 = Button.Button(button_id=1, name="Fold", pos_x=500, pos_y=540)
    btn2 = Button.Button(button_id=2, name="Check", pos_x=640, pos_y=540)
    btn3 = Button.Button(button_id=3, name="Bet", pos_x=780, pos_y=540)

    buttonList.append(btn1)
    buttonList.append(btn2)
    buttonList.append(btn3)


def initialize_cards():
    test_card = deck.draw_card()
    test_card.move_to(100, 100)
    test_card.move(600, 400)
    cardList.append(test_card)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    user_interface.init_display()

    initialize_game_objects()

    while True:
        handle_events()

        clock.tick(60)


if __name__ == '__main__':
    main()
