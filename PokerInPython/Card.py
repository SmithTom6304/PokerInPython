



class Card:

	def __init__(self, number, suit):
		self.model = self.Model(number, suit)
		self.view = None

	def getValue(self):
		return self.model.getValue()

	#Returns true if the card is face up
	def isFaceUp(self):
		return self.model.isFaceUp()

	#Sets the card to be faceup/facedown based on value. Returns false if assertion fails
	def setFaceUp(self, value):
		return self.model.setFaceUp(value)


	class Model:

		def __init__(self, number, suit):
			self.value = {"number": None, "suit": None}
			self.faceUp = False

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

		def setFaceUp(self, value):
			if(value == True):
				self.faceUp = True
				return True
			if(value == False):
				self.faceUp = False
				return True
			return False	#If assignment fails, return false

	class View:

		faceUpImage = None
		faceDownImage = None




	


