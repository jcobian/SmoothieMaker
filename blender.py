import pygame
class Blender(pygame.sprite.Sprite):
	def __init__(self, gs=None,hspeed=0.0,playerNumber=1):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.playerNumber = playerNumber
			if self.playerNumber == 1:
				self.image = pygame.image.load("blender.png")
			elif self.playerNumber == 2:
				self.image = pygame.image.load("blender2.png")
			
			self.rect = self.image.get_rect()

			if self.playerNumber == 1:
				self.rect = self.rect.move(self.gs.width/4,self.gs.height-self.rect.height)
			elif self.playerNumber == 2:
				self.rect = self.rect.move(3*self.gs.width/4,self.gs.height-self.rect.height)



			self.colliderect = self.rect.inflate(-self.rect.width*.18,-self.rect.height*.9)
			self.colliderect = self.colliderect.move((-self.rect.width*.18)/2,(-self.rect.height*.9)/2)
			self.orig_image = self.image
			if self.playerNumber == 1:
				self.leftBound = 0
				self.rightBound = self.gs.width/2
			elif self.playerNumber == 2:
				self.leftBound = self.gs.width/2
				self.rightBound = self.gs.width

			self.hspeed = hspeed
	def tick(self):
		fruitRects = list()
		for fruit in self.gs.fruits:
			fruitRects.append(fruit.rect)
		#indicies = self.colliderect.collidelistall(self.gs.fruits)
		indicies = self.colliderect.collidelistall(fruitRects)
		for index in indicies:
			food = self.gs.fruits[index]
			self.gs.fruits.pop(index)

			if food.type == 'fruit':
				self.gs.addToScore()
			elif food.type == 'vegetable':
				self.gs.subFromScore()






	def move(self,key):
		if key == pygame.K_RIGHT:
			if (self.rect.left + self.rect.width + self.hspeed)<self.rightBound:
				self.rect = self.rect.move(self.hspeed,0)
		
		if key == pygame.K_LEFT:
			if (self.rect.left - self.hspeed) > self.leftBound:
				self.rect = self.rect.move(-self.hspeed,0)


		self.colliderect = self.rect.inflate(-self.rect.width*.18,-self.rect.height*.9)
		self.colliderect = self.colliderect.move((-self.rect.width*.18)/2,(-self.rect.height*.9)/2)


		