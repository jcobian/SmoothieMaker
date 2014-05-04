class FruitData():
	def __init__(self,fruitInt=0,xpos=0,vspeed=0,foodType='fruit',fruitID=0,freezeString=''):
		self.fruitInt = fruitInt
		self.xpos = xpos
		self.vspeed = vspeed
		self.foodType = foodType
		self.fruitID = fruitID
		self.freezeString = freezeString

	def toString(self):
			return str(self.fruitInt) + ":" + str(self.xpos) + ":" + str(self.vspeed) + ":" + self.foodType + ":" + str(self.fruitID) + ":" + self.freezeString