import pygame
class BlackRect(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("blackrect.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(self.gs.width-self.rect.width,self.gs.height-self.rect.height)

	#on each tick, move down the screen
	def tick(self):
		percentage = 1-(self.gs.score/float(self.gs.winningScore))

		#self.rect = self.rect.inflate(0,-self.rect.height*percentage)
		self.rect = self.rect.move(0,(-self.rect.height*percentage)/2)