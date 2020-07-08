import unittest
import Card


class TestCardMethods(unittest.TestCase):
    Card.base_path = "../PokerInPython/"

    def test_smoke(self):
        card = Card.Card(3, 'H')

        self.assertEqual(card.get_value()["number"], 3)
        self.assertEqual(card.get_value()["suit"], 'H')
        self.assertNotEqual(card.get_value()["number"], 5)
        self.assertNotEqual(card.get_value()["suit"], 'C')

    def test_canInitializeCard(self):
        card1 = Card.Card(5, 'S')
        self.assertEqual(card1.get_value()["number"], 5)
        self.assertEqual(card1.get_value()["suit"], 'S')
        self.assertNotEqual(card1.get_value()["number"], 7)
        self.assertNotEqual(card1.get_value()["suit"], 'D')

        card2 = Card.Card(15, 'D')
        self.assertEqual(card2.get_value()["number"], None)

        card3 = Card.Card(10, 'X')
        self.assertEqual(card3.get_value()["suit"], None)

        card4 = Card.Card(8, 20)
        self.assertEqual(card4.get_value()["suit"], None)

    def test_canSetFacedown(self):
        card1 = Card.Card(14, 'S')
        self.assertEqual(card1.is_face_up(), False)

        card1.set_face_up(True)
        self.assertEqual(card1.is_face_up(), True)

        card1.flip()
        self.assertEqual(card1.is_face_up(), False)
        card1.flip()
        self.assertEqual(card1.is_face_up(), True)

    def test_canMoveCardRelative(self):
        card = Card.Card(3, 'H', 10, 20)

        self.assertEqual(10, card.get_rect().x, "Card was not initialized with the correct parameters")
        self.assertEqual(20, card.get_rect().y, "Card was not initialized with the correct parameters")

        card.move_by(30, 0)

        self.assertEqual(40, card.get_rect().x, "Card did not move in the x direction")
        self.assertNotEqual(10, card.get_rect().x, "Card did not move in the x direction")

        card.move_by(0, 15)

        self.assertEqual(35, card.get_rect().y, "Card did not move in the y direction")
        self.assertNotEqual(20, card.get_rect().y, "Card did not move in the y direction")

        card.move_by(-30, -20)

        self.assertEqual(10, card.get_rect().x, "Card did not move negatively in the x direction")
        self.assertEqual(15, card.get_rect().y, "Card did not move negatively in the y direction")

    def test_canMoveCardAbsolute(self):
        card = Card.Card(3, 'H', 10, 20)

        self.assertEqual(10, card.get_rect().x, "Card was not initialized with the correct parameters")
        self.assertEqual(20, card.get_rect().y, "Card was not initialized with the correct parameters")

        card.move_to(30, 0)

        self.assertEqual(30, card.get_rect().x, "Card did not move in the x direction")
        self.assertNotEqual(10, card.get_rect().x, "Card did not move in the x direction")

        card.move_to(0, 15)

        self.assertEqual(15, card.get_rect().y, "Card did not move in the y direction")
        self.assertNotEqual(20, card.get_rect().y, "Card did not move in the y direction")

        card.move_to(-30, -20)

        self.assertEqual(0, card.get_rect().x, "Card did not move negatively in the x direction")
        self.assertEqual(0, card.get_rect().y, "Card did not move negatively in the y direction")

    def test_canSetMoving(self):
        card1 = Card.Card(14, 'S')
        self.assertEqual(card1.is_moving(), False)
        card1.move(100, 100)
        self.assertEqual(card1.is_moving(), True)




if __name__ == '__main__':
    unittest.main()
