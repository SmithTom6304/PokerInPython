import unittest
import Deck

class TestDeckMethods(unittest.TestCase):

	Deck.basepath = "../PokerInPython/"

	def test_smoke(self):
		deck = Deck.Deck()

		self.assertTrue(deck.deck[3].getValue()["number"] != None)

	def test_wholeDeckIsFilled(self):
		deck = Deck.Deck()

		for i in range(0, 52):
			self.assertTrue(deck.deck[i].getValue()["number"] != None)

	# def test_deckIsShuffledRandomly(self):
	# 	deck = Deck.Deck()
	# 	distribution = []

	# 	for x in range(0, 52):
	# 		distribution.append(0)

	# 	n = 100

	# 	for loop in range(0, n):
	# 		deck.resetDeck()

	# 		for i in range(0, 52):
	# 			card = deck.deck[i]
	# 			cardvalue = 0
	# 			cardvalue += (card.getValue()["number"] - 1)
	# 			suit = card.getValue()["suit"]
	# 			if(suit == 'C'):
	# 				cardvalue += 0
	# 			if(suit == 'D'):
	# 				cardvalue += 13
	# 			if(suit == 'H'):
	# 				cardvalue += 26
	# 			if(suit == 'S'):
	# 				cardvalue += 39

	# 			distribution[cardvalue] += i

	# 	distribution.sort()
	# 	#self.assertTrue(25000 < (distribution[51] - distribution[0]) < 27000)
		




if __name__ == '__main__':
	unittest.main()