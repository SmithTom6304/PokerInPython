import pygame



class Button:

	def __init__(self, id, name, posX = 0, posY = 0):
		self.model = self.Model(id, name)
		self.view = self.View(name, posX, posY)

	def getId(self):
		return self.model.getId()

	def getRect(self):
		return self.view.getRect()

	def getName(self):
		return self.model.getName()

	def moveTo(self, x, y):
		self.view.moveAbsolute(x, y)

	def moveBy(self, x, y):
		self.view.moveRelative(x, y)

	def getImage(self):
		return self.view.getImage()

	def getRect(self):
		return self.view.getRect()

	class Model:
		def __init__(self, id, name):
			self.id = id
			self.name = name

		def getId(self):
			return self.id

		def getName(self):
			return self.name


	class View:
		def __init__(self, name, posX, posY):
			ButtonPath = "./Images/Buttons/"
			self.image = pygame.image.load(f"{ButtonPath}Btn_{name}.png")
			self.rect = self.image.get_rect(topleft=(posX, posY))

		def getRect(self):
			return self.rect

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

		#Move a buttons rect coords to an absolute position
		def moveAbsolute(self, x, y):
			if (x >= 0):
				self.rect.x = x
			else:
				self.rect.x = 0

			if (y >= 0):
				self.rect.y = y
			else:
				self.rect.y = 0