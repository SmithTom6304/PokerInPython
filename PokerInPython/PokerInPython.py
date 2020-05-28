import sys
import pygame
import random
import os

import UserInterface
import Card
import Player
import Deck

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
		objectImagesToUpdateQueue.extend(player.getCards())


	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()


	for each in objectImagesToUpdateQueue:
		objectImagesToUpdateSequence.append((each.getImage(), each.getRect()))

	
	UserInterface.updateDisplay(objectImagesToUpdateSequence)


	return


def initializePlayers(numberOfPlayers, chips):
	playerList.clear()

	#player1 = Player.Player(1)

	for i in range(2, numberOfPlayers+1):
		xValue = (width/numberOfPlayers) * (i-1)
		player = Player.Player(i, chips, confidence=100, posX=xValue, posY=(height/6))
		player.setCards([deck.drawCard(), deck.drawCard()])
		playerList.append(player)
	return


def main():


	pygame.init()
	clock = pygame.time.Clock()


	

	#myfont = pygame.font.SysFont('Elephant', 16)
	

	#screen = pygame.display.set_mode(size)

	UserInterface.initDisplay()

	#r1 = random.randint(1, 13)
	#r2 = random.randint(1, 13)
	#s1 = random.randint(0, 3)
	#s2 = random.randint(0, 3)


	#card1 = pygame.image.load(f"{CardPath}Card_{r1}{cSuit[s1]}.png")
	#card2 = pygame.image.load(f"{CardPath}Card_{r2}{cSuit[s2]}.png")
	#card1rect = card1.get_rect(center=((width/2) - 20, height - 80)) #center=((width/2) - 40, height - 150)
	#card2rect = card2.get_rect(center=((width/2) + 20, height - 80)) #topleft=((width/2) + 40, height - 150)

	# c1 = deck.drawCard()
	# c2 = deck.drawCard()
	# c3 = deck.drawCard()
	# c4 = deck.drawCard()
	# c1.moveTo(player2.getRect().x-20, player2.getRect().y)
	# c2.moveTo(player2.getRect().x+20, player2.getRect().y)
	# c3.moveTo(player3.getRect().x-20, player2.getRect().y)
	# c4.moveTo(player3.getRect().x+20, player2.getRect().y)
	# c1.flip()
	# c2.flip()
	# c3.flip()
	# c4.flip()

	# player2.setCards([c1, c2])
	# player3.setCards([c3, c4])

	initializePlayers(3, 100)

	#player1 = Opponent(40, 20, f"{CharacterPath}Player2.png")
	#player1text = myfont.render(str(player1.getChips()), False, (0, 0, 0))
	#player2 = Opponent(388, 20, f"{CharacterPath}Player3.png")
	#player2text = myfont.render(str(player2.getChips()), False, (0, 0, 0))
	#player3 = Opponent(736, 20, f"{CharacterPath}Player4.png")
	#player3text = myfont.render(str(player3.getChips()), False, (0, 0, 0))

	#btnFold = pygame.image.load(f"{ButtonPath}Btn_Fold.png")
	#btnFoldRect = btnFold.get_rect(center=(340, 460))
	#btnCheck = pygame.image.load(f"{ButtonPath}Btn_Check.png")
	#btnCheckRect = btnCheck.get_rect(center=(460, 460))
	#btnRaise = pygame.image.load(f"{ButtonPath}Btn_Raise.png")
	#btnRaiseRect = btnRaise.get_rect(center=(580, 460))

	#fold check raise
	#	  call



	mousepos = [0, 0]

	

	while True:

		handleEvents()
		



		

		

		
		


		#screen.fill(background)
		
			#screen.blit(Card1.image, Card1.rect)
			#screen.blit(Card2.image, Card2.rect)
		#screen.blit(player1.getImage(), player1.getRect())
		#screen.blit(player1text, player1.getRect())
		#screen.blit(player2.getImage(), player2.getRect())
		#screen.blit(player2text, player2.getRect())
		#screen.blit(player3.getImage(), player3.getRect())
		#screen.blit(player3text, player3.getRect())

		#screen.blit(btnFold, btnFoldRect)
		#screen.blit(btnCheck, btnCheckRect)
		#screen.blit(btnRaise, btnRaiseRect)
			#pygame.display.flip()


		clock.tick(30)

if __name__ == '__main__': main()