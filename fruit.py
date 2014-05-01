import pygame
import random
class Fruit(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		#load a random image
		randFruitInt = random.randint(0,len(self.gs.listOfFruitImages)-1)
		fruitImage = self.gs.listOfFruitImages[randFruitInt]
		self.image = pygame.image.load(fruitImage)
		self.rect = self.image.get_rect()

		#get rand x pos
		self.xpos = random.randint(0,self.gs.width-self.rect.width)
		self.ypos = 0
		self.rect = self.rect.move(self.xpos,self.ypos)
		self.orig_image = self.image
		#get rand speed
		self.vspeed = random.randint(3,8)

	#on each tick, move down the screen
	def tick(self):
		self.rect = self.rect.move(0,self.vspeed)
	

