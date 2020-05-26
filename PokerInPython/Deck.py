import Card
import random

class Deck:

	def __init__(self):
		self.deck = []
		self.resetDeck()

	def resetDeck(self):

		self.deck.clear()

		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'C'))
		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'D'))
		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'H'))
		for i in range(1, 14):
			self.deck.append(Card.Card(i, 'S'))

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
