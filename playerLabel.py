import pygame
class PlayerLabel(pygame.sprite.Sprite):
	def __init__(self, gs=None, textLabel, xpos, ypos, size):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.white = 255,255,255
			self.myfont = pygame.font.SysFont("monospace", size)
			self.label = self.myfont.render(textLabel,1,self.white)
			self.rect.center = (xpos, ypos)
			
	def tick(self):
		pass		