import unittest
import Player
import Card


class TestPlayerMethods(unittest.TestCase):

	Player.basepath = "../PokerInPython/"

	def test_smoke(self):
		player = Player.Player(2, 30, 60, 30, 15)

		self.assertEqual(player.getNumber(), 2)
		self.assertEqual(player.getChips(), 30)
		self.assertEqual(player.getConfidence(), 60)
		self.assertNotEqual(player.getNumber(), 5)
		self.assertNotEqual(player.getChips(), 40)
		self.assertNotEqual(player.getConfidence(), 40)

	def test_canMovePlayerRelative(self):
		player = Player.Player(3, 100, 50, 10, 20)


		self.assertEqual(10, player.getRect().x, "Player was not initialized with the correct parameters")
		self.assertEqual(20, player.getRect().y, "Player was not initialized with the correct parameters")

		player.moveBy(30, 0)

		self.assertEqual(40, player.getRect().x, "Player did not move in the x direction")
		self.assertNotEqual(10, player.getRect().x, "Player did not move in the x direction")

		player.moveBy(0, 15)

		self.assertEqual(35, player.getRect().y, "Player did not move in the y direction")
		self.assertNotEqual(20, player.getRect().y, "Player did not move in the y direction")

		player.moveBy(-30, -20)

		self.assertEqual(10, player.getRect().x, "Player did not move negatively in the x direction")
		self.assertEqual(15, player.getRect().y, "Player did not move negatively in the y direction")

	def test_canMovePlayerAbsolute(self):
		player = Player.Player(3, 100, 50, 10, 20)


		self.assertEqual(10, player.getRect().x, "Player was not initialized with the correct parameters")
		self.assertEqual(20, player.getRect().y, "Player was not initialized with the correct parameters")

		player.moveTo(30, 0)

		self.assertEqual(30, player.getRect().x, "Player did not move in the x direction")
		self.assertNotEqual(10, player.getRect().x, "Player did not move in the x direction")

		player.moveTo(0, 15)

		self.assertEqual(15, player.getRect().y, "Player did not move in the y direction")
		self.assertNotEqual(20, player.getRect().y, "Player did not move in the y direction")

		player.moveTo(-30, -20)

		self.assertEqual(0, player.getRect().x, "Player did not move negatively in the x direction")
		self.assertEqual(0, player.getRect().y, "Player did not move negatively in the y direction")

	def test_canAssignCardsToPlayer(self):
		player = Player.Player(3, 100, 50, 10, 20)
		card1 = Card.Card(3, 'H')
		card2 = Card.Card(5, 'D')

		player.setCards([card1, card2])

		playerCard1 = player.getCards()[0]
		playerCard2 = player.getCards()[1]

		self.assertEqual(playerCard1.getValue()["number"], 3)
		self.assertEqual(playerCard1.getValue()["suit"], 'H')
		self.assertEqual(playerCard2.getValue()["number"], 5)
		self.assertEqual(playerCard2.getValue()["suit"], 'D')

	def test_canSetFacedown(self):

		player = Player.Player(3, 100, 50, 10, 20)
		card1 = Card.Card(3, 'H')
		card2 = Card.Card(5, 'D')

		player.setCards([card1, card2])

		playerCard1 = player.getCards()[0]
		playerCard2 = player.getCards()[1]

		self.assertEqual(playerCard1.isFaceUp(), False)

		playerCard1.setFaceUp(True)
		self.assertEqual(playerCard1.isFaceUp(), True)

		playerCard1.flip()
		self.assertEqual(playerCard1.isFaceUp(), False)
		playerCard1.flip()
		self.assertEqual(playerCard1.isFaceUp(), True)


if __name__ == '__main__':
	unittest.main()