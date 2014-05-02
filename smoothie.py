import pygame
from blender import Blender
from fruit import Fruit
from progressBar import ProgressBar
from blackRect import BlackRect
#main gamespace where the overarching game structure is
class GameSpace:
	def __init__(self):
		self.listOfFruitImages=['strawberry.png','banana.png']
		self.listOfVegetableImages = ['potato.png']
		self.listOfFrozenFruitImages = ['strawberryfrozen.png','bananafrozen.png']
		self.listOfFrozenVegetableImages = ['potatofrozen.png']

		self.fruits = list()
		self.score = 0
		self.winningScore = 100 
	def main(self):
		#1) basic initialization
		pygame.init()

		#so that key holds can be recognized.
		pygame.key.set_repeat(17,17)	
		
		self.size = self.width, self.height = 900,900
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)

		
		#2 set up game objects
		self.clock = pygame.time.Clock()
		self.blender = Blender(self,hspeed=5.0)
		self.progressBar = ProgressBar(self)
		self.blackRect = BlackRect(self)

		self.gameObjectsList = list()
		self.gameObjectsList.append(self.blender)
		self.gameObjectsList.append(self.progressBar)
		self.gameObjectsList.append(self.blackRect)
		
		#start game loop
		while 1:
			#4) clock tick regulation
			self.clock.tick(60) #frame rate
			ticks = pygame.time.get_ticks()
			if ticks%60 == 0:
				fruit = Fruit(self,type='fruit')
				self.fruits.append(fruit)
			if ticks % 90 == 0:
				veggie = Fruit(self,type='vegetable')
				self.fruits.append(veggie)

			#handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.blender.move(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mx,my = pygame.mouse.get_pos()
					self.freezeFruits(mx,my)
					

				elif event.type == pygame.QUIT:
					return	

			#6 send a tick to every game object
			for obj in self.gameObjectsList:
				obj.tick()
			for fr in self.fruits:
				fr.tick()
			
			#7 display game objects
			self.screen.fill(self.black)
			for fr in self.fruits:
				self.screen.blit(fr.image,fr.rect)
			for obj in self.gameObjectsList:
				self.screen.blit(obj.image,obj.rect)
			
			

			pygame.display.flip()

	def addToScore(self):
		self.score+=10
		if self.score > self.winningScore:
			self.score = self.winningScore
		self.checkIfWon()
	def subFromScore(self):
		self.score-=20
		if self.score < 0:
			self.score = 0
	def checkIfWon(self):
		if self.score >= self.winningScore:
			print 'won'
	def freezeFruits(self,mx,my):
		for fruit in self.fruits:
			if fruit.rect.collidepoint(mx,my):
				fruit.freezeFruit()


			
		
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()