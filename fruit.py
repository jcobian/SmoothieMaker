import pygame
import random
class Fruit(pygame.sprite.Sprite):
	def __init__(self,gs=None,type='fruit'):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.type = type
		self.frozen = False
		#load a random image
		if self.type == 'fruit':
			self.randFruitInt = random.randint(0,len(self.gs.listOfFruitImages)-1)
			fruitImage = self.gs.listOfFruitImages[self.randFruitInt]
			frozenImage = self.gs.listOfFrozenFruitImages[self.randFruitInt]



		elif self.type == 'vegetable':
			self.randFruitInt = random.randint(0,len(self.gs.listOfVegetableImages)-1)
			fruitImage = self.gs.listOfVegetableImages[self.randFruitInt]
			frozenImage = self.gs.listOfFrozenVegetableImages[self.randFruitInt]



		self.image = pygame.image.load(fruitImage)
		self.rect = self.image.get_rect()

		#get rand x pos
		self.xpos = random.randint(0,self.gs.width-self.rect.width)
		self.ypos = 0
		self.rect = self.rect.move(self.xpos,self.ypos)


		self.orig_image = self.image

		self.frozen_image = pygame.image.load(frozenImage)

		#get rand speed
		self.vspeed = random.randint(3,8)

	#on each tick, move down the screen
	def tick(self):
		if self.frozen == False:
			self.rect = self.rect.move(0,self.vspeed)
			if self.rect.top >= self.gs.height:
				self.gs.fruits.remove(self)
		else:
			current_tick = pygame.time.get_ticks()
			if current_tick - self.startedFreezeTicks >= 1500:
				self.unFreezeFruit()

	def freezeFruit(self):
		if self.frozen == False:
			self.frozen = True
			self.startedFreezeTicks = pygame.time.get_ticks()
			self.image = self.frozen_image
			self.rect = self.image.get_rect(center=self.rect.center)

			

			

	def unFreezeFruit(self):
		self.frozen = False
		self.image = self.orig_image
		self.rect = self.image.get_rect(center=self.rect.center)

				
	

