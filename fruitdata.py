
'''
Jonathan Cobian and Oliver Lamb
Fruit Data class represents data that will be sent (and pickled) over the FruitConn
'''
class FruitData():
	def __init__(self,fruitInt=0,xpos=0,vspeed=0,foodType='fruit',fruitID=0,freezeDirection='',freezeID='',dataType='create'):
		self.dataType = dataType
		if dataType == 'create':
			self.fruitInt = fruitInt
			self.xpos = xpos
			self.vspeed = vspeed
			self.foodType = foodType
			self.fruitID = fruitID
		elif dataType=='freeze':
			self.freezeDirection = freezeDirection
			self.freezeID = freezeID


	