import pygame

basepath = "./"

class Card:

	def __init__(self, number, suit, posX = 0, posY = 0):
		self.model = self.Model(number, suit)
		#Return if failed to assign, most likely because card was assigned with bad values
		if(self.model.getValue()["number"] == None or self.model.getValue()["suit"] == None):
			print("ERROR: Card was not initialized properly")
			return
		self.view = self.View(number, suit, posX, posY)

	def updatePosition(self):
		self.moveStep()

	def getValue(self):
		return self.model.getValue()

	#Returns true if the card is face up
	def isFaceUp(self):
		return self.model.isFaceUp()

	#Sets the card to be faceup/facedown based on value. Returns false if assertion fails
	def setFaceUp(self, value):
		self.view.setImage(value)
		return self.model.setFaceUp(value)

	def flip(self):
		flip_faceup = self.isFaceUp()
		return self.setFaceUp(not flip_faceup)

	def getImage(self):
		return self.view.getImage()

	def getRect(self):
		return self.view.getRect()

	def isMoving(self):
		return self.model.isMoving()

	def move(self, x, y):
		self.view.new_moveAbsolute(x, y)
		self.model.moving = True

	def moveTo(self, x, y):
		self.view.moveAbsolute(x, y)

	def moveBy(self, x, y):
		self.view.moveRelative(x, y)

	def moveStep(self):
		self.view.moveStep()

	def setWaitFrames(self, waitFrames):
		self.view.waitFrames = waitFrames

	





	class Model:

		def __init__(self, number, suit):
			self.value = {"number": None, "suit": None}
			self.faceUp = False
			self.moving = False

			#Ensure given card values are valid. Set to None and return if not. 
			if(number < 1 or number > 13):
				self.number = None
				return
			if(suit != 'H' and suit != 'D' and suit !='C' and suit != 'S'):
				self.suit = None
				return

			self.value["number"] = number
			self.value["suit"] = suit

		def getValue(self):
			return self.value

		def isFaceUp(self):
			return self.faceUp

		def isMoving(self):
			return self.moving

		def setFaceUp(self, value):
			if(value == True):
				self.faceUp = True
				return True
			if(value == False):
				self.faceUp = False
				return True
			return False	#If assignment fails, return false

		def setMoving(self, value):
			if(value == True):
				self.moving = True
				return True
			if(value == False):
				self.moving = False
				return True
			return False	#If assignment fails, return false

	class View:
		
		def __init__(self, number, suit, posX=0, posY=0, waitFrames=0):
			CardPath = f"{basepath}Images/Cards/"
			self.imageFaceUp = pygame.image.load(f"{CardPath}Card_{number}{suit}.png")
			self.imageFaceDown = pygame.image.load(f"{CardPath}Card_Back.png")
			self.image = self.imageFaceDown
			self.rect = self.image.get_rect(topleft=(posX, posY))
			self.waitFrames = waitFrames

			self.movingTo = [0.0, 0.0]

		def setImage(self, faceupValue):
			if(faceupValue == True):
				self.image = self.imageFaceUp
			else:
				self.image = self.imageFaceDown

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

		#Move a cards rect coords to an absolute position
		def moveAbsolute(self, x, y):
			if (x >= 0):
				self.rect.x = x
			else:
				self.rect.x = 0

			if (y >= 0):
				self.rect.y = y
			else:
				self.rect.y = 0

		def new_moveAbsolute(self, x, y):
			if (x >= 0):
				self.movingTo[0] = x
			else:
				self.movingTo[0] = 0

			if (y >= 0):
				self.movingTo[1] = y
			else:
				self.movingTo[1] = 0

		def moveStep(self):

			if(self.waitFrames > 0):
				self.waitFrames-=1
				return

			#Calculate difference between current pos and final pos
			a_rect = self.getRect()
			a_moveTo = self.movingTo
			deltaX = a_moveTo[0] - a_rect.x
			deltaY = a_moveTo[1] - a_rect.y
			stepSize = 10

			#If x or y is close to final x or y, move it there
			if abs(deltaX) < stepSize:
				self.moveAbsolute(a_moveTo[0], a_rect.y)
			if abs(deltaY) < stepSize:
				self.moveAbsolute(a_rect.x, a_moveTo[1])

			#Re-calculate difference between current pos and final pos
			a_rect = self.getRect()
			a_moveTo = self.movingTo
			deltaX = a_moveTo[0] - a_rect.x
			deltaY = a_moveTo[1] - a_rect.y

			#Move towards the final destination
			if(deltaX > 0):
				self.moveRelative(stepSize, 0)
			if(deltaX < 0):
				self.moveRelative(-stepSize, 0)
			if(deltaY > 0):
				self.moveRelative(0, stepSize)
			if(deltaY < 0):
				self.moveRelative(0, -stepSize)

			if(deltaX == 0 and deltaY == 0):
				self.moving = False






	


