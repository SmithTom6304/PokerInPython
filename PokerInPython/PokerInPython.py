import sys
import pygame
import random
import os

import UserInterface
import Card
import Player
import Deck
import Button

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5,35)

size = width, height = 920, 640
speed = [2, 2]
black = 0, 0, 0
background = 49, 117, 61

#Queue of objects to be added to the sequence to update
objectImagesToUpdateQueue = []
#List of (image, rect) tuples to provide to UserInterface layer to update screen
objectImagesToUpdateSequence = [None, None]

playerList = []
buttonList = []
cardList = []

deck = Deck.Deck()

# player2 = Player.Player(2, 300, 50, 230, 30)
# player3 = Player.Player(3, 300, 50, 690, 30)



def handleEvents():

	mousepos = pygame.mouse.get_pos()
	UserInterface.mouse_pos = mousepos

	#Clear the sequence of images that will be updated
	objectImagesToUpdateSequence.clear()
	objectImagesToUpdateQueue.clear()

	# objectImagesToUpdateQueue.append(player2)
	# objectImagesToUpdateQueue.append(player3)
	# objectImagesToUpdateQueue.extend(player2.getCards())
	# objectImagesToUpdateQueue.extend(player3.getCards())

	for player in playerList:
		objectImagesToUpdateQueue.append(player)
		#objectImagesToUpdateQueue.extend(player.getCards())

	for button in buttonList:
		objectImagesToUpdateQueue.append(button)

	for card in cardList:
		if card.isMoving():
			card.moveStep()

		objectImagesToUpdateQueue.append(card)

	objectImagesToUpdateQueue.append(deck)


	


	for each in objectImagesToUpdateQueue:
		objectImagesToUpdateSequence.append((each.getImage(), each.getRect()))

	
	UserInterface.updateDisplay(objectImagesToUpdateSequence)


	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				initializeGameObjects()
			if event.key == pygame.K_RIGHT:
				for each in cardList:
					each.setFaceUp(True)


def initializeGameObjects():
	playerList.clear()
	buttonList.clear()
	cardList.clear()
	deck.resetDeck()

	initializePlayers(4, 100)
	initializeButtons()
	initializeCards()

	#Add wait frames to each card to create ripple effect
	for i in range(0, len(cardList)):
		cardList[i].setWaitFrames((len(cardList)-i) * 3)


def initializePlayers(numberOfPlayers, chips):
	player1 = Player.Player(1, chips, confidence=100, posX = 80, posY = 400)
	player1.setCards([deck.drawCard(), deck.drawCard()])
	player1.setCardsFaceUp(True)
	playerList.append(player1)
	cardList.extend(player1.getCards())

	for i in range(2, numberOfPlayers+1):
		xValue = (width/numberOfPlayers) * (i-1)
		player = Player.Player(i, chips, confidence=100, posX=xValue, posY=(height/6))
		player.setCards([deck.drawCard(), deck.drawCard()])
		playerList.append(player)
		cardList.extend(player.getCards())
	

def initializeButtons():
	btn1 = Button.Button(id=1, name="Fold", posX= 500, posY=540)
	btn2 = Button.Button(id=2, name="Check", posX= 640, posY=540)
	btn3 = Button.Button(id=3, name="Bet", posX= 780, posY=540)

	buttonList.append(btn1)
	buttonList.append(btn2)
	buttonList.append(btn3)
	

def initializeCards():
	testCard = deck.drawCard()
	testCard.moveTo(100, 100)
	testCard.move(600, 400)
	cardList.append(testCard)


def main():


	pygame.init()
	clock = pygame.time.Clock()



	UserInterface.initDisplay()

	initializeGameObjects()

	


	mousepos = [0, 0]

	

	while True:

		handleEvents()
		



		clock.tick(60)

if __name__ == '__main__': main()