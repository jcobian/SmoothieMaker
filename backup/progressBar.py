import pygame
class ProgressBar(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("progressbar.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(self.gs.width-self.rect.width,self.gs.height-self.rect.height)

	#on each tick, move down the screen
	def tick(self):
		pass		


		

	

