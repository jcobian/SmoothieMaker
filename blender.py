class Blender(pygame.sprite.Sprite):
	def __init__(self, gs=None,hspeed=0.0):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.image = pygame.image.load("blender.png")
			self.rect = self.image.get_rect()
			self.rect = self.rect.move(self.gs.width/2,self.gs.height-self.rect.get_height())
			self.orig_image = self.image

			self.hspeed = hspeed

	def move(self,key):
		if key == pygame.K_RIGHT:
			self.rect = self.rect.move(self.hspeed,0)		
		if key == pygame.K_LEFT:
			self.rect = self.rect.move(-self.hspeed,0)		
		