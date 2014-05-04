from twisted.internet import protocol,reactor
from twisted.internet.task import LoopingCall
import sys
import pickle
from smoothie import GameSpace
from twisted.internet.defer import DeferredQueue
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


class FruitConn(protocol.Protocol):
	def __init__(self,client):
		self.client = client
		self.fruitQueue = DeferredQueue()
		self.fruitQueue.get().addCallback(self.sendMyData)

	def freezeFruit(self,fruitID):
		self.transport.write('Freeze:'+str(self.playerNumber)+':'+str(fruitID)+':norm')

	def freezeOppFruit(self,fruitID):
		self.transport.write('Freeze:'+str(self.playerNumber)+':'+str(fruitID)+':opp')

	def sendMyData(self,fruitData):
		datapd =  pickle.dumps(fruitData)
		theString = str(self.playerNumber)+':'+datapd
		comp = theString.split(':')
		self.transport.write(theString)

	def readyForMore(self):
		self.fruitQueue.get().addCallback(self.sendMyData)
	
		
	def connectionMade(self):
		self.client.fruitConn = self
		print 'Connection succesfully made to the server'
		self.transport.write('start')

	def closeConn(self):
		reactor.stop()

	def dataReceived(self,data):
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

		elif data == 'ready for more':
			self.readyForMore()
		elif data.startswith('Freeze'):
			comp = data.split(':')
			fruitID = int(comp[2])
			freezeType = comp[3]
			if freezeType == 'opp':
				self.gs.freezeOpponentFruitWithID(fruitID)
			else:
				self.gs.freezeFruitWithID(fruitID)
		else:
			self.parseData(data)

	def parseData(self,data):
		try:
			comp = data.split(':')
			fruitData = pickle.loads(comp[1])
			self.gs.addFruit(fruitData.fruitInt,fruitData.xpos,fruitData.vspeed,fruitData.foodType,fruitData.fruitID)
			self.transport.write('added fruit:'+str(self.playerNumber))
		except:
			print 'Error'

			 
	def gameOver(self,text):
		self.lc = LoopingCall(self.gs.goToGameOver,(text))
		self.lc.start(1/60)



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



	
