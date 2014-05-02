import pygame
class PlayerLabel(pygame.sprite.Sprite):
	def __init__(self, gs=None, textLabel="", xpos=0, ypos=0, size=0):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.white = 255,255,255
			self.myfont = pygame.font.SysFont("monospace", size)
			self.label = self.myfont.render(textLabel,1,self.white)
			self.textPos = self.label.get_rect()
			self.rect = (xpos-self.textPos.width/2, ypos-self.textPos.height/2)

	def tick(self):
		pass