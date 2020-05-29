import Card
import random
import pygame

class Deck:

	def __init__(self):
		CardPath = "./Images/Cards/"
		self.deck = []
		self.image = pygame.image.load(f"{CardPath}Card_Deck.png")
		self.rect = self.image.get_rect(topleft=(100, 400))
		self.resetDeck()
		
		

	def resetDeck(self):

		self.deck.clear()

		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'C', self.rect.x, self.rect.y))
		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'D', self.rect.x, self.rect.y))
		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'H', self.rect.x, self.rect.y))
		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'S', self.rect.x, self.rect.y))

		self.shuffleDeck()


	#Function taken from https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/
	def shuffleDeck(self):

		arr = self.deck

		n = len(arr)
		for i in range(n-1, 0, -1):
			j = random.randint(0, i)

			#print(arr[i].getValue()["number"])
			#print(arr[j].getValue()["number"])
			#print(f"i = {i}")
			#print(f"j = {j}")

			try:
				arr[i], arr[j] = arr[j], arr[i]
			except Exception as e:
				print(f"i = {i}")
				print(f"j = {j}")

		self.deck = arr

	def drawCard(self):
		return self.deck.pop()

	def getImage(self):
		return self.image

	def getRect(self):
		return self.rect
