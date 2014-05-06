'''
Jonathan Cobian and Oliver Lamb
Client is a wrapper for the connections to the server
Fruit Conn sends information about the creation of fruits and when fruits are frozen
Blender Conn sends the player's current position constantly to update it to the opponent's screen
'''

from twisted.internet import protocol,reactor
from twisted.internet.task import LoopingCall
from twisted.protocols.basic import LineReceiver
import sys
import pickle
from smoothie import GameSpace
from twisted.internet.defer import DeferredQueue
from fruitdata import FruitData
class Client():
	def __init__(self,host,fruitPort,blenderPort):
		self.host = host
		self.fruitPort = fruitPort
		self.blenderPort = blenderPort
		self.fruitConn = None
		self.blenderConn = None
		reactor.connectTCP(self.host,self.blenderPort,BlenderConnFactory(self))
		reactor.connectTCP(self.host,self.fruitPort,FruitConnFactory(self))

		reactor.run()



class FruitConn(LineReceiver):
	def __init__(self,client):
		self.client = client
		self.fruitQueue = DeferredQueue()
		self.fruitQueue.get().addCallback(self.sendMyData)

	#sends the data over to the server
	def sendMyData(self,fruitData):	
			datapd =  pickle.dumps(fruitData)
			theString = str(self.playerNumber)+':'+datapd
			self.sendLine(theString)
			self.fruitQueue.get().addCallback(self.sendMyData)

	def connectionMade(self):
		self.client.fruitConn = self
		print 'Connection succesfully made to the server'
		self.sendLine('start')
		#self.transport.write('start')

	def closeConn(self):
		reactor.stop()

	#whenever data is received
	def lineReceived(self,data):
		#will happen if server only has one player connected (you)
		if data == 'waiting for players':
			print 'Waiting for another player..'
		elif data == 'lost conn':
			print 'Connection was lost, sorry'
			reactor.stop()
		#will happen if server has two connection. Will send your player number over (PN) along with random seed
		elif data.startswith('PN'):
			comp = data.split(':')
			self.playerNumber = int(comp[1])
			#so that both clients have the same seed to create fruits
			self.randSeed = int(comp[2])
			self.minFruitSpeed = int(comp[3])
			self.maxFruitSpeed = int(comp[4])
			self.client.blenderConn.playerNumber = self.playerNumber
			if self.playerNumber == 1:
				print 'Game Started: You are the Pink Player'
			else:
				print 'Game Started: You are the Green Player'

			#create the gamespace and start the loop
			self.gs = GameSpace(self,self.playerNumber,self.randSeed,self.minFruitSpeed,self.maxFruitSpeed)
			self.client.blenderConn.gs = self.gs
			self.gs.main()
			self.lc = LoopingCall(self.gs.countDown)
			self.lc.start(1/60)
			#start sending blender data continuously
			self.client.blenderConn.sendMyData()
		#when you receive gameplay data (will either be to add a fruit or freeze a fruit)
		else:
			self.parseData(data)




	def parseData(self,data):
		comp = data.split(':')
		fruitData = pickle.loads(comp[1])
		if fruitData.dataType == 'create':
			self.gs.addFruit(fruitData.fruitInt,fruitData.xpos,fruitData.vspeed,fruitData.foodType,fruitData.fruitID)
		#freeze type
		else:
			if fruitData.freezeDirection == 'left':
				self.gs.freezeLeftFruitWithID(fruitData.freezeID)
			else:
				self.gs.freezeRightFruitWithID(fruitData.freezeID)
	
	#will be called after the countdown finishes
	def startGameLoop(self):
		self.lc.stop()
		self.lc = LoopingCall(self.gs.gameLoopIteration)
		self.lc.start(1/60)

	#will be called once someone wins
	def gameOver(self,text):
		self.lc = LoopingCall(self.gs.goToGameOver,(text))
		self.lc.start(1/60)

	#called from gamespace whenever they click on a fruit on the right side of their screen
	def freezeLeftFruit(self,fruitID):
		fruitData = FruitData(dataType='freeze',freezeDirection='left',freezeID=fruitID)
		self.fruitQueue.put(fruitData)

	#called from gamespace whenever they click on a fruit on the left side of their screen
	def freezeRightFruit(self,fruitID):
		fruitData = FruitData(dataType='freeze',freezeDirection='right',freezeID=fruitID)
		self.fruitQueue.put(fruitData)



#continually sends blender data (position)
class BlenderConn(protocol.Protocol):
	def __init__(self,client):
		self.client = client
		self.playerNumber = 0
		self.gs = None

	def connectionMade(self):
		self.client.blenderConn = self

	def sendMyData(self):
		pd = pickle.dumps(self.gs.blender.rect)
		score = self.gs.score
		theString = str(self.playerNumber)+':'+pd+':'+str(score)
		comp = theString.split(':')
		self.transport.write(theString)

	def closeConn(self):
		reactor.stop()

	def dataReceived(self,data):
		if data == 'lost conn':
			print 'Connection was lost, sorry'
		else:
			self.parseData(data) #get position
			self.sendMyData() #send next position

	def parseData(self,data):
		comp = data.split(':')
		pd = comp[1]
		rect = pickle.loads(pd)
		#update opponents position on your screen
		self.gs.updateOpponent(rect)
		#update opponents score on your screen
		oppScore = int(comp[2])
		self.gs.opponentScore = oppScore
		

			 
		
		

	

class FruitConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return FruitConn(self.client)

class BlenderConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return BlenderConn(self.client)

if __name__ == '__main__':
	if len(sys.argv) <4:
		print 'usage: python client.py <host machine> <port 1> <port 2>'
		sys.exit()
	host = sys.argv[1]
	fruitPort = int(sys.argv[2])
	blenderPort = int(sys.argv[3])
		
	client = Client(host,fruitPort,blenderPort)



	
