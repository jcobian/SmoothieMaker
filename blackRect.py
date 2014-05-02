import pygame
class BlackRect(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("blackrect.png")
		self.rect = self.image.get_rect()
		self.orig_rect = self.rect
		self.rect = self.rect.move(self.gs.width-self.rect.width,self.gs.height-self.rect.height)
		print 'init:',self.rect.top,self.rect.height
		self.currentPercentage = 0
	#on each tick, move down the screen
	def tick(self):
		percentage = (self.gs.score/float(self.gs.winningScore))
		if self.currentPercentage != percentage:
			print 'percentage',percentage
			#self.rect = self.rect.inflate(0,-self.orig_rect.height*percentage)
			self.rect = self.orig_rect.move(0,(-self.orig_rect.height*percentage))
			print 'tick:',self.rect.top,self.rect.height
			self.currentPercentage = percentage

