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

	def sendMyData(self,fruitData):	
			datapd =  pickle.dumps(fruitData)
			theString = str(self.playerNumber)+':'+datapd
			self.sendLine(theString)
			#self.transport.write(theString)
			self.fruitQueue.get().addCallback(self.sendMyData)
		
	def connectionMade(self):
		self.client.fruitConn = self
		print 'Connection succesfully made to the server'
		self.sendLine('start')
		#self.transport.write('start')

	def closeConn(self):
		reactor.stop()

	def lineReceived(self,data):
		if data == 'waiting for players':
			print 'Waiting for another player..'
		elif data == 'lost conn':
			print 'Connection was lost, sorry'
			reactor.stop()
		elif data.startswith('PN'):
			comp = data.split(':')
			self.playerNumber = int(comp[1])
			self.randSeed = int(comp[2])
			self.client.blenderConn.playerNumber = self.playerNumber
			if self.playerNumber == 1:
				print 'Game Started: You are the Pink Player'
			else:
				print 'Game Started: You are the Green Player'

			self.gs = GameSpace(self,self.playerNumber,self.randSeed)
			self.client.blenderConn.gs = self.gs
			self.gs.main()
			self.lc = LoopingCall(self.gs.gameLoopIteration)
			self.lc.start(1/60)
			self.client.blenderConn.sendMyData()
		else:
			self.parseData(data)




	def parseData(self,data):
		try:
			comp = data.split(':')
			fruitData = pickle.loads(comp[1])
			if fruitData.dataType == 'create':
				self.gs.addFruit(fruitData.fruitInt,fruitData.xpos,fruitData.vspeed,fruitData.foodType,fruitData.fruitID)
			else:
				if fruitData.freezeDirection == 'left':
					self.gs.freezeLeftFruitWithID(fruitData.freezeID)
				else:
					self.gs.freezeRightFruitWithID(fruitData.freezeID)
			#self.fruitQueue.get().addCallback(self.sendMyData)
			#self.transport.write('finished fruit data:'+str(self.playerNumber))
			
		except Exception as ex:
			print 'Error!'
			print str(ex)
			print comp


	def gameOver(self,text):
		self.lc = LoopingCall(self.gs.goToGameOver,(text))
		self.lc.start(1/60)


	def freezeLeftFruit(self,fruitID):
		fruitData = FruitData(dataType='freeze',freezeDirection='left',freezeID=fruitID)
		self.fruitQueue.put(fruitData)

	def freezeRightFruit(self,fruitID):
		fruitData = FruitData(dataType='freeze',freezeDirection='right',freezeID=fruitID)
		self.fruitQueue.put(fruitData)




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
			self.parseData(data)
			self.sendMyData()

	def parseData(self,data):
		comp = data.split(':')
		pd = comp[1]
		rect = pickle.loads(pd)
		self.gs.updateOpponent(rect)
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
	host = sys.argv[1]
	fruitPort = int(sys.argv[2])
	blenderPort = int(sys.argv[3])
	client = Client(host,fruitPort,blenderPort)



	
