import unittest
import Player
import Card


class TestPlayerMethods(unittest.TestCase):
    Player.base_path = "../PokerInPython/"

    def test_smoke(self):
        player = Player.Player(2, 30, 60, 30, 15)

        self.assertEqual(player.get_number(), 2)
        self.assertEqual(player.get_chips(), 30)
        self.assertEqual(player.get_confidence(), 60)
        self.assertNotEqual(player.get_number(), 5)
        self.assertNotEqual(player.get_chips(), 40)
        self.assertNotEqual(player.get_confidence(), 40)

    def test_canMovePlayerRelative(self):
        player = Player.Player(3, 100, 50, 10, 20)

        self.assertEqual(10, player.get_rect().x, "Player was not initialized with the correct parameters")
        self.assertEqual(20, player.get_rect().y, "Player was not initialized with the correct parameters")

        player.move_by(30, 0)

        self.assertEqual(40, player.get_rect().x, "Player did not move in the x direction")
        self.assertNotEqual(10, player.get_rect().x, "Player did not move in the x direction")

        player.move_by(0, 15)

        self.assertEqual(35, player.get_rect().y, "Player did not move in the y direction")
        self.assertNotEqual(20, player.get_rect().y, "Player did not move in the y direction")

        player.move_by(-30, -20)

        self.assertEqual(10, player.get_rect().x, "Player did not move negatively in the x direction")
        self.assertEqual(15, player.get_rect().y, "Player did not move negatively in the y direction")

    def test_canMovePlayerAbsolute(self):
        player = Player.Player(3, 100, 50, 10, 20)

        self.assertEqual(10, player.get_rect().x, "Player was not initialized with the correct parameters")
        self.assertEqual(20, player.get_rect().y, "Player was not initialized with the correct parameters")

        player.move_to(30, 0)

        self.assertEqual(30, player.get_rect().x, "Player did not move in the x direction")
        self.assertNotEqual(10, player.get_rect().x, "Player did not move in the x direction")

        player.move_to(0, 15)

        self.assertEqual(15, player.get_rect().y, "Player did not move in the y direction")
        self.assertNotEqual(20, player.get_rect().y, "Player did not move in the y direction")

        player.move_to(-30, -20)

        self.assertEqual(0, player.get_rect().x, "Player did not move negatively in the x direction")
        self.assertEqual(0, player.get_rect().y, "Player did not move negatively in the y direction")

    def test_canAssignCardsToPlayer(self):
        player = Player.Player(3, 100, 50, 10, 20)
        card1 = Card.Card(3, 'H')
        card2 = Card.Card(5, 'D')

        player.set_cards([card1, card2])

        playerCard1 = player.get_cards()[0]
        playerCard2 = player.get_cards()[1]

        self.assertEqual(playerCard1.get_value()["number"], 3)
        self.assertEqual(playerCard1.get_value()["suit"], 'H')
        self.assertEqual(playerCard2.get_value()["number"], 5)
        self.assertEqual(playerCard2.get_value()["suit"], 'D')

    def test_canSetFacedown(self):
        player = Player.Player(3, 100, 50, 10, 20)
        card1 = Card.Card(3, 'H')
        card2 = Card.Card(5, 'D')

        player.set_cards([card1, card2])

        playerCard1 = player.get_cards()[0]
        # playerCard2 = player.get_cards()[1]


        self.assertEqual(playerCard1.is_face_up(), False)

        playerCard1.set_face_up(True)
        self.assertEqual(playerCard1.is_face_up(), True)

        playerCard1.flip()
        self.assertEqual(playerCard1.is_face_up(), False)
        playerCard1.flip()
        self.assertEqual(playerCard1.is_face_up(), True)


if __name__ == '__main__':
    unittest.main()
