class FruitData():
	def __init__(self,fruitInt=0,xpos=0,vspeed=0,foodType='fruit',fruitID=0,freezeDirection='',freezeID='',dataType='create'):
		if dataType == 'create':
			self.fruitInt = fruitInt
			self.xpos = xpos
			self.vspeed = vspeed
			self.foodType = foodType
			self.fruitID = fruitID
			self.dataType = dataType
		elif dataType=='freeze':
			self.freezeString = freezeString
			self.freezeDirection = freezeDirection
			self.freezeID = freezeID

	def toString(self):
			return str(self.fruitInt) + ":" + str(self.xpos) + ":" + str(self.vspeed) + ":" + self.foodType + ":" + str(self.fruitID) + ":" + self.freezeString