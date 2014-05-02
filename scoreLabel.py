import pygame
class ScoreLabel(pygame.sprite.Sprite):
	def __init__(self, gs=None,playerType='user'):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.white = 255,255,255
			self.myfont = pygame.font.SysFont("monospace",50)
			self.label = self.myfont.render("0%",1,self.white)
			self.playerType = playerType

			if self.playerType == 'user':
				self.rect = (0,50)
			elif self.playerType == 'opponent':
				self.rect = (0,self.gs.width-50)
			

	def tick(self):
		if self.playerType == 'user':
			percentage = self.gs.score/float(self.gs.winningScore)
		else:
			percentage = self.gs.opponentScore/float(self.gs.winningScore)
		self.setScore(percentage*100)

	def setScore(self,score):
		scoreString = str(score)+"%"
		self.label = self.myfont.render(scoreString,1,self.white)

		


