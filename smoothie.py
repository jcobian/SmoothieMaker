import pygame
import random
import sys
from blender import Blender
from fruit import Fruit
from progressBar import ProgressBar
from blackRect import BlackRect
from scoreLabel import ScoreLabel
#main gamespace where the overarching game structure is
class GameSpace:
	def __init__(self,commandConn,playerNumber):
		self.commandConn = commandConn
		self.listOfFruitImages=['strawberry.png','banana.png']
		self.listOfVegetableImages = ['potato.png']
		self.listOfFrozenFruitImages = ['strawberryfrozen.png','bananafrozen.png']
		self.listOfFrozenVegetableImages = ['potatofrozen.png']
		self.playerNumber = playerNumber
		self.fruits = list()
		self.score = 0
		self.winningScore = 100 

		self.size = self.width, self.height = 1280,800
		self.black = 0,0,0
		self.white = 255,255,255
		self.point1 = self.width/2,0
		self.point2 = self.width/2,self.height


	def main(self):
		#1) basic initialization
		pygame.init()

		#so that key holds can be recognized.
		pygame.key.set_repeat(17,17)	
		
		

		self.screen = pygame.display.set_mode(self.size)
		self.current_ticks = 0
		
		#2 set up game objects
		self.clock = pygame.time.Clock()
		#get playernumber from server

		self.blender = Blender(self,hspeed=7.0,playerNumber=self.playerNumber,playerType='user')
		opponentPlayerNumber = 1
		if self.playerNumber == 1:
			opponentPlayerNumber = 2

		self.opponent = Blender(self,hspeed=7.0,playerNumber=opponentPlayerNumber,playerType='opponent')

		#self.progressBar = ProgressBar(self)
		#self.blackRect = BlackRect(self)
		self.scoreLabel = ScoreLabel(self)
		self.scoreLabelPlayer2 = ScoreLabel(self)

		self.gameObjectsList = list()
		self.gameObjectsList.append(self.blender)
		#self.gameObjectsList.append(self.progressBar)
		#self.gameObjectsList.append(self.blackRect)
		
	
		#start game loop
		#while 1:
			#runs an iteration, returns 1 if they hit quit button
			#if self.gameLoopIteration():
				#return

	def gameLoopIteration(self):
		#4) clock tick regulation
		#self.clock.tick(60) #frame rate
		if self.current_ticks%60 == 0:
			randFruitInt = random.randint(0,len(self.listOfFruitImages)-1)
			xpos = random.randint(0,self.width/2)
			vspeed = random.randint(3,6)
			fruit = Fruit(self,type='fruit',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
			xpos += self.width/2
			fruit2 = Fruit(self,type='fruit',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
			self.fruits.append(fruit)
			self.fruits.append(fruit2)

		if self.current_ticks % 90 == 0:
			xpos = random.randint(0,self.width/2)
			randFruitInt = random.randint(0,len(self.listOfVegetableImages)-1)
			vspeed = random.randint(3,6)
			veggie = Fruit(self,type='vegetable',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
			xpos+=self.width/2
			veggie2 = Fruit(self,type='vegetable',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
			self.fruits.append(veggie)
			self.fruits.append(veggie2)

		#handle user inputs
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.blender.move(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mx,my = pygame.mouse.get_pos()
				self.freezeFruits(mx,my)
			elif event.type == pygame.QUIT:
				return 1	

		#6 send a tick to every game object
		for obj in self.gameObjectsList:
			obj.tick()
		for fr in self.fruits:
			fr.tick()
		self.scoreLabel.tick()
		self.scoreLabelPlayer2.tick()
		
		#7 display game objects
		self.screen.fill(self.black)


		self.screen.blit(self.scoreLabel.label,self.scoreLabel.rect)
		self.screen.blit(self.scoreLabelPlayer2.label,self.scoreLabelPlayer2.rect)


		for fr in self.fruits:
			self.screen.blit(fr.image,fr.rect)
		for obj in self.gameObjectsList:
			self.screen.blit(obj.image,obj.rect)
		self.screen.blit(self.opponent.image,self.opponent.rect)
		pygame.draw.line(self.screen,self.white,self.point1,self.point2)
			
		
		

		pygame.display.flip()
		self.current_ticks+=1
		return 0
		
	def updateOpponent(self,rect):
		self.opponent.rect = rect
	def addToScore(self):
		self.score+=10
		if self.score > self.winningScore:
			self.score = self.winningScore
		self.checkIfWon()
	def subFromScore(self):
		self.score-=20
		if self.score < 0:
			self.score = 0
	def checkIfWon(self):
		if self.score >= self.winningScore:
			print 'won'
	def freezeFruits(self,mx,my):
		for fruit in self.fruits:
			if fruit.rect.collidepoint(mx,my):
				fruit.freezeFruit()


			
		

