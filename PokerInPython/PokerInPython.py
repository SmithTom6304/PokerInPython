import sys
import pygame
import random
import os

import UserInterface

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5,35)

size = width, height = 920, 640
speed = [2, 2]
black = 0, 0, 0
background = 49, 117, 61

test = "f"

CardPath = "./Images/Cards/"
ButtonPath = "./Images/Buttons/"
CharacterPath = "./Images/Characters/"

cNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
cSuit = ['H', 'D', 'C', 'S']

class Opponent:
	rect = None
	image = None
	card = [None, None]
	chips = 100
	confidence = 0
	cool = 0
	def __init__(self, x, y, image):
		self.image = pygame.image.load(image)
		chips = 100
		confidence = 1
		cool = 1
		self.rect = self.image.get_rect(topleft=(x, y))
	def getChips(self):
		return self.chips

	def getRect(self):
		return self.rect

	def getImage(self):
		return self.image

	def getCards(self):
		return self.card

	def clearCards(self):
		card = [None, None]


class Player:
	card = [None, None]
	def __init__(self):
		chips = 100
	def getChips(self):
		return self.chips

	def getCards(self):
		return self.card

	def clearCards(self):
		card = [None, None]


def shuffleDeck():
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

	Card1 = UserInterface.Card(3, 'S', (width/2) - 20, height - 160)
	Card2 = UserInterface.Card(5, 'H', (width/2) + 20, height - 160)

	
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

	c1rect = Card1.getRect()
	card1pos = [c1rect.x, c1rect.y]
	c2rect = Card2.getRect()
	card2pos = [c2rect.x, c2rect.y]


	mousepos = [0, 0]

	sequence = [None, None]

	while True:
		mousepos = pygame.mouse.get_pos()

		sequence.clear()

		Card1.moveAbsolute(card1pos[0], card1pos[1])
		

		Card2.moveAbsolute(card2pos[0], card2pos[1])
		


		

		


		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		if (Card1.rect.collidepoint(mousepos) and not Card2.rect.collidepoint(mousepos)):
			Card1.moveRelative(0, -10)

		if Card2.rect.collidepoint(mousepos):
			Card2.moveRelative(0, -10)

		
		
		sequence.append((Card1.image, Card1.rect))
		sequence.append((Card2.image, Card2.rect))
	
		UserInterface.updateDisplay(sequence)


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