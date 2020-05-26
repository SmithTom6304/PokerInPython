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