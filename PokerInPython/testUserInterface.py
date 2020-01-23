import unittest
import UserInterface
import pygame


class TestCardMethods(unittest.TestCase):

	def test_smoke(self):
		card = UserInterface.Card(3, 'H', 10, 20)

		self.assertEqual(card.getNumber(), 3)
		self.assertEqual(card.getSuit(), 'H')
		self.assertEqual(card.rect.x, 10)
		self.assertEqual(card.rect.y, 20)

	def test_canMoveCardRelative(self):
		card = UserInterface.Card(3, 'H', 10, 20)


		self.assertEqual(10, card.rect.x, "Card was not initialized with the correct parameters")
		self.assertEqual(20, card.rect.y, "Card was not initialized with the correct parameters")

		card.moveRelative(30, 0)

		self.assertEqual(40, card.rect.x, "Card did not move in the x direction")
		self.assertNotEqual(10, card.rect.x, "Card did not move in the x direction")

		card.moveRelative(0, 15)

		self.assertEqual(35, card.rect.y, "Card did not move in the y direction")
		self.assertNotEqual(20, card.rect.y, "Card did not move in the y direction")

		card.moveRelative(-30, -20)

		self.assertEqual(10, card.rect.x, "Card did not move negatively in the x direction")
		self.assertEqual(15, card.rect.y, "Card did not move negatively in the y direction")

	def test_canMoveCardAbsolute(self):
		card = UserInterface.Card(3, 'H', 10, 20)


		self.assertEqual(10, card.rect.x, "Card was not initialized with the correct parameters")
		self.assertEqual(20, card.rect.y, "Card was not initialized with the correct parameters")

		card.moveAbsolute(30, 0)

		self.assertEqual(30, card.rect.x, "Card did not move in the x direction")
		self.assertNotEqual(10, card.rect.x, "Card did not move in the x direction")

		card.moveAbsolute(0, 15)

		self.assertEqual(15, card.rect.y, "Card did not move in the y direction")
		self.assertNotEqual(20, card.rect.y, "Card did not move in the y direction")

		card.moveAbsolute(-30, -20)

		self.assertEqual(0, card.rect.x, "Card did not move negatively in the x direction")
		self.assertEqual(0, card.rect.y, "Card did not move negatively in the y direction")

	def test_canInitializeScreen(self):
		UserInterface.initDisplay()
		UserInterface.screen.fill(UserInterface.background)

		self.assertTrue(UserInterface.screen)

	def test_canUpdateDisplay(self):
		UserInterface.initDisplay()
		image = pygame.image.load(f"./Images/Cards/Card_3S.png")
		rect = image.get_rect(topleft=(0, 0))

		UserInterface.screen.blit(image, rect)



if __name__ == '__main__':
	unittest.main()