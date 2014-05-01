import pygame
#main gamespace where the overarching game structure is
class GameSpace:
	def main(self):
		#1) basic initialization
		pygame.init()

		#so that key holds can be recognized.
		pygame.key.set_repeat(17,17)	
		
		self.size = self.width, self.height = 640,480
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)

		
		#2 set up game objects
		self.clock = pygame.time.Clock()
		self.gameObjectsList = list()
		
		#start game loop
		while 1:
			#4) clock tick regulation
			self.clock.tick(60) #frame rate
		
			#handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.player.fire(self.laserList)
					else:
						self.player.move(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.player.fire(self.laserList)
				elif event.type == pygame.MOUSEBUTTONUP:
					self.player.stopFire()
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						self.player.stopFire()
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
			
		
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()