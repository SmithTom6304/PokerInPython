#UserInterface layer
import sys
import pygame

size = width, height = 920, 640
screen = None

black = 0, 0, 0
background = 49, 117, 61

CardPath = "./Images/Cards/"
ButtonPath = "./Images/Buttons/"
CharacterPath = "./Images/Characters/"

cNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
cSuit = ['H', 'D', 'C', 'S']

#myfont = pygame.font.SysFont('Elephant', 16)

class Card:
	number = None
	suit = None

	image = None
	rect = None

	def __init__(self, number, suit, posX=0, posY=0):
		self.number = number
		self.suit = suit

		self.image = pygame.image.load(f"{CardPath}Card_{number}{suit}.png")
		self.rect = self.image.get_rect(topleft=(posX, posY))

	def getRect(self):
		return self.rect


	def getNumber(self):
		return self.number

	def getSuit(self):
		return self.suit

	#Move a cards rect coords relative to the current coords
	def moveRelative(self, x=0, y=0):
		if ((self.rect.x + x) >= 0):
			self.rect.x += x
		else:
			self.rect.x = 0

		if ((self.rect.y + y) >= 0):
			self.rect.y += y
		else:
			self.rect.y = 0

	#Move a cards rect coords to an absolute position
	def moveAbsolute(self, x=0, y=0):
		if (x >= 0):
			self.rect.x = x
		else:
			self.rect.x = 0

		if (y >= 0):
			self.rect.y = y
		else:
			self.rect.y = 0





def initDisplay():
	global screen 
	screen = pygame.display.set_mode(size)
	return

def updateDisplay(sequence):

	screen.fill(background)

	screen.blits(sequence)
	

	pygame.display.flip()

	return