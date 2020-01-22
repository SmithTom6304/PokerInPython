import unittest
import UserInterface

class TestCardMethods(unittest.TestCase):

	def test_smoke(self):
		card = UserInterface.Card(3, 'H', 10, 20)

		self.assertEqual(card.getNumber(), 3)
		self.assertEqual(card.getSuit(), 'H')
		self.assertEqual(card.rect.x, 10)
		self.assertEqual(card.rect.y, 20)


if __name__ == '__main__':
	unittest.main()