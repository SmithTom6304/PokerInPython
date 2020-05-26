import pygame

class Player:
	

	def __init__(self, number, chips, confidence, posX, posY):
		self.model = self.Model(number, chips, confidence)
		self.view = self.View(number, posX, posY)

	def getNumber(self):
		return self.model.getNumber()

	def getChips(self):
		return self.model.getChips()

	def getConfidence(self):
		return self.model.getConfidence()

	def getImage(self):
		return self.view.getImage()

	def getRect(self):
		return self.view.getRect()

	def moveTo(self, x, y):
		self.view.moveAbsolute(x, y)

	def moveBy(self, x, y):
		self.view.moveRelative(x, y)



	class Model:

		def __init__(self, number, chips, confidence):
			self.number = number
			self.chips = chips
			self. confidence = confidence

		def getNumber(self):
			return self.number

		def getChips(self):
			return self.chips

		def getConfidence(self):
			return self.confidence


	class View:
		
		def __init__(self, number, posX, posY):
			CharacterPath = "./Images/Characters/"
			self.image = pygame.image.load(f"{CharacterPath}Player{number}.png")
			self.rect = self.image.get_rect(topleft=(posX, posY))

		def getImage(self):
			return self.image

		def getRect(self):
			return self.rect

		def moveRelative(self, x, y):

			if ((self.rect.x + x) >= 0):
				self.rect.x += x
			else:
				self.rect.x = 0

			if ((self.rect.y + y) >= 0):
				self.rect.y += y
			else:
				self.rect.y = 0

		#Move a players rect coords to an absolute position
		def moveAbsolute(self, x, y):
			if (x >= 0):
				self.rect.x = x
			else:
				self.rect.x = 0

			if (y >= 0):
				self.rect.y = y
			else:
				self.rect.y = 0
