import pygame
import random
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

		#get rand x starting pos
		#self.xpos = random.randint(0,self.gs.width/2-self.rect.width)
		self.xpos = xpos-self.rect.width
		self.ypos = -self.rect.height-10 #start it a little bit above the screen
		self.rect = self.rect.move(self.xpos,self.ypos)

		self.orig_image = self.image

		self.frozen_image = pygame.image.load(frozenImage)

		#get rand speed
		self.vspeed = vspeed
		self.current_tick = 0

		self.start = False

	#on each tick, move down the screen if you're not frozen
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

	def doTheTick(self):
		if self.frozen == False:
			self.rect = self.rect.move(0,self.vspeed)
			if self.rect.top >= self.gs.height:
				if self.side == 'left':
					self.gs.fruits.remove(self)
				else:
					self.gs.fruitsOpp.remove(self)
		else:
			self.current_tick+=1
			#after certain timedelay, unfreeze yourself
			if self.current_tick >= 180:
				self.unFreezeFruit()
		

	def freezeFruit(self):
		#only want to freeze a fruit that is unfrozen
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
	def updateFruit(self,imageName,frozen,rect,vspeed,currentTicks):
		self.image = pygame.image.load(imageName)
		self.frozen = frozen
		self.rect = rect
		self.vspeed = vspeed
		self.current_tick = currentTicks



				
	

