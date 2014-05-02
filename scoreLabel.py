import pygame
class ScoreLabel(pygame.sprite.Sprite):
	def __init__(self, gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.white = 255,255,255
			self.myfont = pygame.font.SysFont("monospace",50)
			self.label = self.myfont.render("0%",1,self.white)
			self.rect = (0,50)
			

	def tick(self):
		percentage = self.gs.score/float(self.gs.winningScore)
		self.setScore(percentage*100)

	def setScore(self,score):
		scoreString = str(score)+"%"
		self.label = self.myfont.render(scoreString,1,self.white)

		


