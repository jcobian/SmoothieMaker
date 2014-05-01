import pygame
from blender import Blender
from fruit import Fruit
#main gamespace where the overarching game structure is
class GameSpace:
	def __init__(self):
		self.listOfFruitImages=['strawberry.png','banana.png']
		self.listOfVegetableImages = list()
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

		self.gameObjectsList = list()
		self.gameObjectsList.append(self.blender)
		counter = 0
		#start game loop
		while 1:
			#4) clock tick regulation
			self.clock.tick(60) #frame rate
			if pygame.time.get_ticks() % 60 == 0:
				fruit = Fruit(self)
				self.gameObjectsList.append(fruit)
			#handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.blender.move(event.key)
				elif event.type == pygame.QUIT:
					return	

			#6 send a tick to every game object
			for object in self.gameObjectsList:
				object.tick()
			
			
			#7 display game objects
			self.screen.fill(self.black)
			for object in self.gameObjectsList:
				self.screen.blit(object.image,object.rect)
			pygame.display.flip()
			counter+=1
			
		
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()