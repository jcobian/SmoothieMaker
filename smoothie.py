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
	def __init__(self,fruitConn,playerNumber,randSeed):
		#reference to the connection to the server
		self.fruitConn = fruitConn

		self.playerNumber = playerNumber
		random.seed(randSeed)

		#list of images
		self.listOfFruitImages=['strawberry.png','banana.png','raspberry.png','blueberry.png']
		self.listOfVegetableImages = ['potato.png', 'onion.png','broccoli.png']
		self.listOfFrozenFruitImages = ['strawberryfrozen.png','bananafrozen.png','raspberryfrozen.png','blueberryfrozen.png']
		self.listOfFrozenVegetableImages = ['potatofrozen.png', 'frozenonion.png','broccolifrozen.png']
		self.goldenImage = 'pineapple.png'
		self.frozenGoldImage = 'pineapplefrozen.png'

		#list of your fruits and opponents fruits (the ones on the right)
		self.fruits = list()
		self.fruitsOpp = list()


		self.score = 0
		self.opponentScore = 0
		self.winningScore = 200 

		#for screen drawings
		self.size = self.width, self.height = 1280,800
		self.black = 0,0,0
		self.white = 255,255,255
		#to draw the white veritcal line down the middle
		self.point1 = self.width/2,0
		self.point2 = self.width/2,self.height

		
		

		self.counter = 0
		


	def main(self):
		#1) basic initialization
		pygame.init()

		#so that key holds can be recognized.
		pygame.key.set_repeat(17,17)	
		
		

		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('Smoothie Maker')
		#counter of ticks
		self.current_ticks = 0
		
		#2 set up game objects
		self.clock = pygame.time.Clock()

		#create the blender object that represents you
		self.blender = Blender(self,hspeed=7.0,playerNumber=self.playerNumber,playerType='user')

		opponentPlayerNumber = 1
		if self.playerNumber == 1:
			opponentPlayerNumber = 2

		#create the blender object that represents your opponent
		self.opponent = Blender(self,hspeed=7.0,playerNumber=opponentPlayerNumber,playerType='opponent')

		self.scoreLabel = ScoreLabel(self,playerType='user')
		self.scoreLabelOpponent = ScoreLabel(self,playerType='opponent')

		self.youLabel = PlayerLabel(self,textLabel="You",xpos=self.width/4,ypos=40,size=50)
		self.oppLabel = PlayerLabel(self,textLabel="Opponent",xpos=3*self.width/4,ypos=40,size=50)
	





		self.gameObjectsList = list()
		self.gameObjectsList.append(self.blender)
		self.gameObjectsList.append(self.opponent)

		self.gameLabels = list()
		self.gameLabels.append(self.scoreLabel)
		self.gameLabels.append(self.scoreLabelOpponent)
		self.gameLabels.append(self.youLabel)
		self.gameLabels.append(self.oppLabel)

		
	def countDown(self):
		self.screen.fill(self.black)
		text = "3"
		message = 'You are the pink player on the left'
		if self.playerNumber == 2:
			message = 'You are the green player on the left'
		playerLabel = PlayerLabel(self,textLabel=message,xpos=self.width/2,ypos = self.height/2+100,size=50)
		if self.current_ticks <60:
			text = "3"
		elif self.current_ticks < 120:
			text = "2"
		elif self.current_ticks < 180:
			text = "1"
		else:
			self.fruitConn.startGameLoop()
			return 0

		numLabel = PlayerLabel(self,textLabel=text,xpos=self.width/2,ypos=self.height/2,size=50)
		#handle user inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				self.fruitConn.lc.stop()
				self.fruitConn.closeConn()
				return 1

		self.current_ticks+=1
		gameLabel = PlayerLabel(self,textLabel="Smoothie Maker",xpos=self.width/2,ypos= 100,size=50)
		self.screen.blit(numLabel.label,numLabel.rect)
		self.screen.blit(playerLabel.label,playerLabel.rect)
		self.screen.blit(gameLabel.label,gameLabel.rect)


		pygame.display.flip()

	def gameLoopIteration(self):
		#if you or opponent won, stop the looping call and tell the connection which will generate a new looping call
		if self.score >= self.winningScore:
			self.fruitConn.lc.stop()
			if self.opponentScore>= self.winningScore:
				self.fruitConn.gameOver('Tie!')
			else:
				self.fruitConn.gameOver('You Won')
			return 0
		elif self.opponentScore >= self.winningScore:
			self.fruitConn.lc.stop()
			self.fruitConn.gameOver('Opponent Won')
			return 0
		#otherwise game is not over
		else:
			#every 1 second generate a fruit
			if self.current_ticks%60 == 0:
				self.foodType = 'fruit'
				#10% chance of getting a gold fruit (which is worth double)
				goldRandNum = random.randint(0,9)
				if goldRandNum == 0:
					randFruitInt = -1
				else:
					randFruitInt = random.randint(0,len(self.listOfFruitImages)-1)

				#get random data to create a fruit
				#rand fruit int will determine which image is loaded
				self.randFruitInt = randFruitInt
				#random position of where it will start on x axis
				xpos = random.randint(0,self.width/2)
				self.randXPos = xpos
				#random velocity
				vspeed = random.randint(3,6)
				self.randVSpeed = vspeed
				#give it a unique id
				self.fruitID = self.counter
				self.counter+=1
				#create the fruit
				fruitToAdd = Fruit(self,type=self.foodType,xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed,fruitID=self.fruitID,side='left')
				#create the data you want to pickle over to the other player so he has the same fruit
				fruitData = FruitData(fruitInt=self.randFruitInt,xpos=self.randXPos,vspeed=self.randVSpeed,foodType=self.foodType,fruitID=self.fruitID)
				#add the fruit data over to connection's queue so it can send it over to server (then to other player)
				self.fruitConn.fruitQueue.put(fruitData)
				self.fruits.append(fruitToAdd)
				

			#every 1.67 seconds generate a veggie, do same thing as above
			if self.current_ticks %100 == 0:
				self.foodType = 'vegetable'
				randFruitInt = random.randint(0,len(self.listOfVegetableImages)-1)
				self.randFruitInt = randFruitInt
				xpos = random.randint(0,self.width/2)
				self.randXPos = xpos
				vspeed = random.randint(3,6)
				self.randVSpeed = vspeed
				self.fruitID = self.counter
				self.counter+=1
				fruitToAdd = Fruit(self,type=self.foodType,xpos=xpos,randFruitInt=randFruitInt,vspeed=vspeed,fruitID=self.fruitID,side='left')
				fruitData = FruitData(fruitInt=self.randFruitInt,xpos=self.randXPos,vspeed=self.randVSpeed,foodType=self.foodType,fruitID=self.fruitID)
				self.fruitConn.fruitQueue.put(fruitData)
				self.fruits.append(fruitToAdd)

			
		
			#handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.blender.move(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					#get mouse click and see if it collides with a fruit on the screen
					mx,my = pygame.mouse.get_pos()
					self.freezeFruits(mx,my)
				elif event.type == pygame.QUIT:
					pygame.display.quit()
					self.fruitConn.lc.stop()
					self.fruitConn.closeConn()
					return 1

			#6 send a tick to every game object
			for obj in self.gameObjectsList:
				obj.tick()
			for fr in self.fruits:
				fr.tick()
			for fr in self.fruitsOpp:
				fr.tick()
			for label in self.gameLabels:
				label.tick()

			self.scoreLabel.tick()
			self.scoreLabelOpponent.tick()
			self.youLabel.tick()
			self.oppLabel.tick()
			
			#7 display game objects
			self.screen.fill(self.black)

			for label in self.gameLabels:
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
			#draw white line down the middle
			pygame.draw.line(self.screen,self.white,self.point1,self.point2)
			pygame.display.flip()
			self.current_ticks+=1
			return 0

	#will be the looping call once the game ends
	def goToGameOver(self,text):
		self.screen.fill(self.black)
		winnerLabel = PlayerLabel(self,textLabel=text,xpos=self.width/2,ypos=self.height/2,size=50)
		#handle user inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				self.fruitConn.lc.stop()
				self.fruitConn.closeConn()
				return 1

		self.screen.blit(winnerLabel.label,winnerLabel.rect)
		pygame.display.flip()

	#adds a fruit to your screen, this is a fruit sent over by your opponent which he generated
	def addFruit(self,fruitInt,xpos,vspeed,foodType,iD):
		xpos+=self.width/2
		food = Fruit(self,type=foodType,xpos=xpos,randFruitInt=fruitInt,vspeed=vspeed,fruitID=iD,side='right')
		self.fruitsOpp.append(food)


	#updates the rectangle of the opponent blender on your screen
	def updateOpponent(self,rect):
		self.opponent.rect = rect
		self.opponent.rect = self.opponent.rect.move(self.width/2,0)
		self.opponent.colliderect = self.opponent.rect.inflate(-self.opponent.rect.width*.18,-self.opponent.rect.height*.9)
		self.opponent.colliderect = self.opponent.colliderect.move((-self.opponent.rect.width*.18)/2,(-self.opponent.rect.height*.9)/2)
	
	#add and subtract to your score
	def addToScore(self,double=False):
		self.score+=10
		if double == True:
			self.score+=10

		if self.score > self.winningScore:
			self.score = self.winningScore

	def subFromScore(self):
		self.score-=20
		if self.score < 0:
			self.score = 0
	#will freeze any fruit at mx,my. called when get a click
	def freezeFruits(self,mx,my):
		for fruit in self.fruits:
			if fruit.rect.collidepoint(mx,my):
				fruit.freezeFruit()
				self.fruitConn.freezeRightFruit(fruit.fruitID)

		for fruit in self.fruitsOpp:
			if fruit.rect.collidepoint(mx,my):
				fruit.freezeFruit()
				self.fruitConn.freezeLeftFruit(fruit.fruitID)

	#freezes a fruit w/ given id
	def freezeLeftFruitWithID(self,fruitID):
		for fruit in self.fruits:
			if fruit.fruitID == fruitID:
				fruit.freezeFruit()
	def freezeRightFruitWithID(self,fruitID):
		for fruit in self.fruitsOpp:
			if fruit.fruitID == fruitID:
				fruit.freezeFruit()



			
		

