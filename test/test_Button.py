import unittest
import Button


class TestButtonMethods(unittest.TestCase):
    Button.base_path = "../PokerInPython/"

    def test_smoke(self):
        # print(os.getcwd())

        button = Button.Button(button_id=1, name="Bet", pos_x=30, pos_y=30)

        self.assertEqual(button.get_button_id(), 1)
        self.assertEqual(button.get_name(), "Bet")
        self.assertEqual(button.get_rect().x, 30)

    def test_canMoveButtonRelative(self):
        button = Button.Button(button_id=1, name="Call", pos_x=10, pos_y=20)

        self.assertEqual(10, button.get_rect().x, "Button was not initialized with the correct parameters")
        self.assertEqual(20, button.get_rect().y, "Button was not initialized with the correct parameters")

        button.move_by(30, 0)

        self.assertEqual(40, button.get_rect().x, "Button did not move in the x direction")
        self.assertNotEqual(10, button.get_rect().x, "Button did not move in the x direction")

        button.move_by(0, 15)

        self.assertEqual(35, button.get_rect().y, "Button did not move in the y direction")
        self.assertNotEqual(20, button.get_rect().y, "Button did not move in the y direction")

        button.move_by(-30, -20)

        self.assertEqual(10, button.get_rect().x, "Button did not move negatively in the x direction")
        self.assertEqual(15, button.get_rect().y, "Button did not move negatively in the y direction")

    def test_canMoveButtonAbsolute(self):
        button = Button.Button(button_id=1, name="Call", pos_x=10, pos_y=20)

        self.assertEqual(10, button.get_rect().x, "Button was not initialized with the correct parameters")
        self.assertEqual(20, button.get_rect().y, "Button was not initialized with the correct parameters")

        button.move_to(30, 0)

        self.assertEqual(30, button.get_rect().x, "Button did not move in the x direction")
        self.assertNotEqual(10, button.get_rect().x, "Button did not move in the x direction")

        button.move_to(0, 15)

        self.assertEqual(15, button.get_rect().y, "Button did not move in the y direction")
        self.assertNotEqual(20, button.get_rect().y, "Button did not move in the y direction")

        button.move_to(-30, -20)

        self.assertEqual(0, button.get_rect().x, "Button did not move negatively in the x direction")
        self.assertEqual(0, button.get_rect().y, "Button did not move negatively in the y direction")

    def test_canMouseOverButton(self):
        button = Button.Button(button_id=1, name="Call", pos_x=10, pos_y=20)
        self.assertTrue(button.is_mouse_over(15, 35))
        button.move_to(400, 500)
        self.assertFalse(button.is_mouse_over(15, 35))
        self.assertTrue(button.is_mouse_over(410, 520))

if __name__ == '__main__':
    unittest.main()
