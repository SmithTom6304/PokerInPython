import unittest
import Card


class TestCardMethods(unittest.TestCase):

	def test_smoke(self):
		card = Card.Card(3, 'H')

		self.assertEqual(card.getValue()["number"], 3)
		self.assertEqual(card.getValue()["suit"], 'H')
		self.assertNotEqual(card.getValue()["number"], 5)
		self.assertNotEqual(card.getValue()["suit"], 'C')

	def test_canInitializeCard(self):
		card1 = Card.Card(5, 'S')
		self.assertEqual(card1.getValue()["number"], 5)
		self.assertEqual(card1.getValue()["suit"], 'S')
		self.assertNotEqual(card1.getValue()["number"], 7)
		self.assertNotEqual(card1.getValue()["suit"], 'D')

		card2 = Card.Card(15, 'D')
		self.assertEqual(card2.getValue()["number"], None)

		card3 = Card.Card(10, 'X')
		self.assertEqual(card3.getValue()["suit"], None)

		card4 = Card.Card(8, 20)
		self.assertEqual(card4.getValue()["suit"], None)

	def test_canSetFacedown(self):
		card1 = Card.Card(1, 'S')
		self.assertEqual(card1.isFaceUp(), False)

		card1.setFaceUp(True)
		self.assertEqual(card1.isFaceUp(), True)


if __name__ == '__main__':
	unittest.main()