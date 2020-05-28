import unittest
import Button

class TestButtonMethods(unittest.TestCase):

	def test_smoke(self):
		button = Button.Button(id=1, name="Bet", posX=30, posY=30)

		self.assertEqual(button.getId(), 1)
		self.assertEqual(button.getName(), "Bet")
		self.assertEqual(button.getRect().x, 30)

	def test_canMoveButtonRelative(self):
		button = Button.Button(id=1, name="Call", posX=10, posY=20)


		self.assertEqual(10, button.getRect().x, "Button was not initialized with the correct parameters")
		self.assertEqual(20, button.getRect().y, "Button was not initialized with the correct parameters")

		button.moveBy(30, 0)

		self.assertEqual(40, button.getRect().x, "Button did not move in the x direction")
		self.assertNotEqual(10, button.getRect().x, "Button did not move in the x direction")

		button.moveBy(0, 15)

		self.assertEqual(35, button.getRect().y, "Button did not move in the y direction")
		self.assertNotEqual(20, button.getRect().y, "Button did not move in the y direction")

		button.moveBy(-30, -20)

		self.assertEqual(10, button.getRect().x, "Button did not move negatively in the x direction")
		self.assertEqual(15, button.getRect().y, "Button did not move negatively in the y direction")

	def test_canMoveButtonAbsolute(self):
		button = Button.Button(id=1, name="Call", posX=10, posY=20)


		self.assertEqual(10, button.getRect().x, "Button was not initialized with the correct parameters")
		self.assertEqual(20, button.getRect().y, "Button was not initialized with the correct parameters")

		button.moveTo(30, 0)

		self.assertEqual(30, button.getRect().x, "Button did not move in the x direction")
		self.assertNotEqual(10, button.getRect().x, "Button did not move in the x direction")

		button.moveTo(0, 15)

		self.assertEqual(15, button.getRect().y, "Button did not move in the y direction")
		self.assertNotEqual(20, button.getRect().y, "Button did not move in the y direction")

		button.moveTo(-30, -20)

		self.assertEqual(0, button.getRect().x, "Button did not move negatively in the x direction")
		self.assertEqual(0, button.getRect().y, "Button did not move negatively in the y direction")


if __name__ == '__main__':
	unittest.main()