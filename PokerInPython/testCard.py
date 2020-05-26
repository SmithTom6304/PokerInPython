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

		card1.flip()
		self.assertEqual(card1.isFaceUp(), False)
		card1.flip()
		self.assertEqual(card1.isFaceUp(), True)

	def test_canMoveCardRelative(self):
		card = Card.Card(3, 'H', 10, 20)


		self.assertEqual(10, card.getRect().x, "Card was not initialized with the correct parameters")
		self.assertEqual(20, card.getRect().y, "Card was not initialized with the correct parameters")

		card.moveBy(30, 0)

		self.assertEqual(40, card.getRect().x, "Card did not move in the x direction")
		self.assertNotEqual(10, card.getRect().x, "Card did not move in the x direction")

		card.moveBy(0, 15)

		self.assertEqual(35, card.getRect().y, "Card did not move in the y direction")
		self.assertNotEqual(20, card.getRect().y, "Card did not move in the y direction")

		card.moveBy(-30, -20)

		self.assertEqual(10, card.getRect().x, "Card did not move negatively in the x direction")
		self.assertEqual(15, card.getRect().y, "Card did not move negatively in the y direction")

	def test_canMoveCardAbsolute(self):
		card = Card.Card(3, 'H', 10, 20)


		self.assertEqual(10, card.getRect().x, "Card was not initialized with the correct parameters")
		self.assertEqual(20, card.getRect().y, "Card was not initialized with the correct parameters")

		card.moveTo(30, 0)

		self.assertEqual(30, card.getRect().x, "Card did not move in the x direction")
		self.assertNotEqual(10, card.getRect().x, "Card did not move in the x direction")

		card.moveTo(0, 15)

		self.assertEqual(15, card.getRect().y, "Card did not move in the y direction")
		self.assertNotEqual(20, card.getRect().y, "Card did not move in the y direction")

		card.moveTo(-30, -20)

		self.assertEqual(0, card.getRect().x, "Card did not move negatively in the x direction")
		self.assertEqual(0, card.getRect().y, "Card did not move negatively in the y direction")



if __name__ == '__main__':
	unittest.main()