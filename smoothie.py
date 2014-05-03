import pygame
import random
import pickle
import sys
from blender import Blender
from fruit import Fruit
from progressBar import ProgressBar
from blackRect import BlackRect
from scoreLabel import ScoreLabel
from playerLabel import PlayerLabel
from fruitdata import FruitData
#main gamespace where the overarching game structure is
class GameSpace:
	def __init__(self,commandConn,playerNumber):
		self.commandConn = commandConn
		self.listOfFruitImages=['strawberry.png','banana.png']
		self.listOfVegetableImages = ['potato.png', 'onion.png']
		self.listOfFrozenFruitImages = ['strawberryfrozen.png','bananafrozen.png']
		self.listOfFrozenVegetableImages = ['potatofrozen.png', 'frozenonion.png']
		self.playerNumber = playerNumber
		self.fruits = list()
		self.fruitsOpp = list()
		self.score = 0
		self.opponentScore = 0
		self.winningScore = 100 

		self.size = self.width, self.height = 1280,800
		self.black = 0,0,0
		self.white = 255,255,255
		self.point1 = self.width/2,0
		self.point2 = self.width/2,self.height
		self.gameIsOver = False


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
		self.scoreLabel = ScoreLabel(self,playerType='user')
		self.scoreLabelOpponent = ScoreLabel(self,playerType='opponent')

		self.youLabel = PlayerLabel(self,textLabel="You",xpos=self.width/4,ypos=10,size=50)
		self.oppLabel = PlayerLabel(self,textLabel="Opponent",xpos=3*self.width/4,ypos=10,size=50)


		self.gameObjectsList = list()
		self.gameObjectsList.append(self.blender)

		self.quitGame = False
		self.shouldSendData = 0
		


	def goToGameOver(self,text):
		self.screen.fill(self.black)
		winnerLabel = PlayerLabel(self,textLabel=text,xpos=self.width/2,ypos=self.height/2,size=50)


		#handle user inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				self.commandConn.lc.stop()
				self.commandConn.closeConn()
				return 1

		self.screen.blit(winnerLabel.label,winnerLabel.rect)
		pygame.display.flip()




	def gameLoopIteration(self):
		if self.score >= self.winningScore:
			self.commandConn.lc.stop()
			self.commandConn.gameOver('You Won')
			return 0
		elif self.opponentScore >= self.winningScore:
			self.commandConn.lc.stop()
			self.commandConn.gameOver('Opponent Won')
			return 0
		else:
			if self.current_ticks%120 == 0:
				self.foodType = 'fruit'
				randFruitInt = random.randint(0,len(self.listOfFruitImages)-1)
				self.randFruitInt = randFruitInt
				xpos = random.randint(0,self.width/2)
				self.randXPos = xpos
				vspeed = random.randint(3,6)
				self.randVSpeed = vspeed
				fruit = Fruit(self,type='fruit',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
				fruitData = FruitData(self.randFruitInt,self.randXPos,self.randVSpeed,self.foodType)
				self.commandConn.fruitQueue.put(fruitData)
				xpos += self.width/2
				fruit2 = Fruit(self,type='fruit',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
				print self.playerNumber,'is creating:',self.randFruitInt,self.randXPos,self.randVSpeed,self.foodType
				self.fruits.append(fruit)
				self.fruitsOpp.append(fruit2)
				self.shouldSendData = 1

			'''
			if self.current_ticks % 180 == 0:
				self.foodType = 'vegetable'
				xpos = random.randint(0,self.width/2)
				self.xpos = xpos
				randFruitInt = random.randint(0,len(self.listOfVegetableImages)-1)
				self.randFruitInt = randFruitInt
				vspeed = random.randint(3,6)
				self.randVSpeed = vspeed
				veggie = Fruit(self,type='vegetable',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
				xpos+=self.width/2
				veggie2 = Fruit(self,type='vegetable',xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed)
				print self.playerNumber,'is creating:',self.randFruitInt,self.randXPos,self.randVSpeed,self.foodType

				self.fruits.append(veggie)
				self.fruitsOpp.append(veggie2)
				self.shouldSendData = 1
			'''
			
		
			#handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.blender.move(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mx,my = pygame.mouse.get_pos()
					self.freezeFruits(mx,my)
				elif event.type == pygame.QUIT:
					pygame.display.quit()
					self.commandConn.lc.stop()
					#self.commandConn.transport.write('player quit')
					self.commandConn.closeConn()
					return 1

			#6 send a tick to every game object
			for obj in self.gameObjectsList:
				obj.tick()
			for fr in self.fruits:
				fr.tick()
			for fr in self.fruitsOpp:
				fr.tick()
			self.scoreLabel.tick()
			self.scoreLabelOpponent.tick()
			self.youLabel.tick()
			self.oppLabel.tick()
			
			#7 display game objects
			self.screen.fill(self.black)


			self.screen.blit(self.scoreLabel.label,self.scoreLabel.rect)
			self.screen.blit(self.scoreLabelOpponent.label,self.scoreLabelOpponent.rect)
			self.screen.blit(self.youLabel.label,self.youLabel.rect)
			self.screen.blit(self.oppLabel.label,self.oppLabel.rect)



			for fr in self.fruits:
				self.screen.blit(fr.image,fr.rect)
			for fr in self.fruitsOpp:
				self.screen.blit(fr.image,fr.rect)

			for obj in self.gameObjectsList:
				self.screen.blit(obj.image,obj.rect)
			self.screen.blit(self.opponent.image,self.opponent.rect)
			pygame.draw.line(self.screen,self.white,self.point1,self.point2)
				
			
			

			pygame.display.flip()
			self.current_ticks+=1
			return 0
		

	def addFruit(self,fruitInt,xpos,vspeed,foodType):
		food = Fruit(self,type=foodType,xpos=xpos,randFruitInt=fruitInt,vspeed=vspeed)
		xpos+=self.width/2
		food2 = Fruit(self,type=foodType,xpos=xpos,randFruitInt=fruitInt,vspeed=vspeed)
		self.fruits.append(food)
		self.fruitsOpp.append(food2)
	'''
	def updateMyFruits(self,fruitsList):
		del self.fruits[:]
		for fd in fruitsList:
			imageName = fd['image']
			frozen = fd['frozen']
			rect = pickle.loads(fd['rect'])
			vspeed = fd['vspeed']
			currentTicks = fd['currentTicks']
			fruit = Fruit(gs=self)
			fruit.updateFruit(imageName,frozen,rect,vspeed,currentTicks)
			self.fruits.append(fruit)
	def updateOppFruits(self,fruitsList):
		del self.fruitsOpp[:]
		for fd in fruitsList:
			imageName = fd['image']
			frozen = fd['frozen']
			rect = pickle.loads(fd['rect'])
			print 'in update',rect.top
			vspeed = fd['vspeed']
			currentTicks = fd['currentTicks']
			fruit = Fruit(gs=self)
			fruit.updateFruit(imageName,frozen,rect,vspeed,currentTicks)
			self.fruitsOpp.append(fruit)
			self.commandConn.closeConn()
	'''


	def updateOpponent(self,rect):
		self.opponent.rect = rect
		self.opponent.rect = self.opponent.rect.move(self.width/2,0)
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


			
		

