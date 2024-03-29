
'''
Jonathan Cobian and Oliver Lamb
Fruit class represents a fruit OR a vegetable
'''
import pygame
class Fruit(pygame.sprite.Sprite):
	def __init__(self,gs=None,type='fruit',xpos= 0,randFruitInt=0,vspeed=3,fruitID=0,side='left'):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.type = type
		self.frozen = False
		self.fruitID = fruitID
		self.side = side
		#load a random image
		self.randFruitInt = randFruitInt
		if self.type == 'fruit':
			#will be passed in as -1 if it should be a golden fruit (worth 2x points)
			if self.randFruitInt == -1:
				self.fruitImage = self.gs.goldenImage
				frozenImage = self.gs.frozenGoldImage
			else:	
				self.fruitImage = self.gs.listOfFruitImages[self.randFruitInt]
				frozenImage = self.gs.listOfFrozenFruitImages[self.randFruitInt]
		elif self.type == 'vegetable':
			self.fruitImage = self.gs.listOfVegetableImages[self.randFruitInt]
			frozenImage = self.gs.listOfFrozenVegetableImages[self.randFruitInt]



		self.image = pygame.image.load(self.fruitImage)
		self.rect = self.image.get_rect()

		#adjust x position if necessary 
		if side == 'left':
			if xpos+self.rect.width>=self.gs.width/2:
				self.xpos = xpos-self.rect.width
			else:
				self.xpos = xpos
		elif side == 'right':
			if xpos+self.rect.width>=self.gs.width:
				self.xpos = xpos-self.rect.width
			else:
				self.xpos = xpos

		self.ypos = -self.rect.height-10 #start it a little bit above the screen so not visible
		self.rect = self.rect.move(self.xpos,self.ypos)

		self.orig_image = self.image

		self.frozen_image = pygame.image.load(frozenImage)

		self.vspeed = vspeed
		self.current_tick = 0

		self.start = False #will be true once both this fruit and its counterpart on the other client have been created

	
	def tick(self):
		if self.start == True:
			self.doTheTick()
		else:
			otherList = list()
			if self.side == 'left':
				otherList = self.gs.fruitsOpp
			else:
				otherList = self.gs.fruits

			for fr in otherList:
				if fr.fruitID == self.fruitID:
					self.start = True
					self.doTheTick()
					break
	#the actual tick for each fruit
	#on each tick, move down the screen if you're not frozen
	def doTheTick(self):
		if self.frozen == False:
			self.rect = self.rect.move(0,self.vspeed)
			#remove the fruit once its fallen off the screen
			if self.rect.top >= self.gs.height:
				if self.side == 'left':
					self.gs.fruits.remove(self)
				else:
					self.gs.fruitsOpp.remove(self)
		else: #fruit is frozen
			self.current_tick+=1
			#after certain timedelay (3 seconds), unfreeze yourself
			if self.current_tick >= 180:
				self.unFreezeFruit()
		

	def freezeFruit(self):
		#only want to freeze a fruit that is unfrozen (if they click on a frozen fruit nothing happens)
		if self.frozen == False:
			self.frozen = True
			self.image = self.frozen_image
			self.rect = self.image.get_rect(center=self.rect.center)

	#will unfreeze the fruit
	def unFreezeFruit(self):
		self.frozen = False
		self.image = self.orig_image
		self.rect = self.image.get_rect(center=self.rect.center)
		self.current_tick = 0




				
	

