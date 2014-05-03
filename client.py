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
		reactor.connectTCP(self.host,self.blenderPort,BlenderConnFactory(self))
		reactor.connectTCP(self.host,self.fruitPort,FruitConnFactory(self))
		reactor.run()


class FruitConn(protocol.Protocol):
	def __init__(self,client):
		self.client = client
		self.fruitQueue = DeferredQueue()
		self.fruitQueue.get().addCallback(self.sendMyData)


	def sendMyData(self,fruitData):
		datapd =  pickle.dumps(fruitData)
		theString = str(self.playerNumber)+':'+datapd
		comp = theString.split(':')
		self.transport.write(theString)

	def readyForMore(self):
		self.fruitQueue.get().addCallback(self.sendMyData)
	
		
	def connectionMade(self):
		self.transport.write('connect')

	def closeConn(self):
		reactor.stop()

	def dataReceived(self,data):

		if data == 'waiting for players':
			print 'Waiting for another player..'
		elif data == 'lost conn':
			print 'Your opponent lost their connection, sorry'
			reactor.stop()
		elif data.startswith('PN'):
			comp = data.split(':')
			self.playerNumber = int(comp[1])
			print 'Game Started: You are Player',self.playerNumber
			self.gs = GameSpace(self,self.playerNumber)
			self.gs.main()
			self.lc = LoopingCall(self.gs.gameLoopIteration)
			self.lc.start(1/60)

		elif data == 'ready for more':
			self.readyForMore()
			
		else:
			self.parseData(data)

	def parseData(self,data):
		comp = data.split(':')
		fruitData = pickle.loads(comp[1])
		self.gs.addFruit(fruitData.fruitInt,fruitData.xpos,fruitData.vspeed,fruitData.foodType)
		self.transport.write('added fruit:'+str(self.playerNumber))

			 
	def gameOver(self,text):
		self.lc = LoopingCall(self.gs.goToGameOver,(text))
		self.lc.start(1/60)



class BlenderConn(protocol.Protocol):
	def __init__(self,client):
		self.client = client


	def sendMyData(self,fruitData):
		pd = pickle.dumps(self.gs.blender.rect)
		score = self.gs.score
		
		theString = str(self.playerNumber)+':'+pd+':'+str(score)
		comp = theString.split(':')
		self.transport.write(theString)



		
		
	def closeConn(self):
		reactor.stop()

	def dataReceived(self,data):
		self.parseData(data)
		self.sendMyData()

	def parseData(self,data):
		comp = data.split(':')
		pd = comp[1]
		opponent = pickle.loads(pd)
		self.gs.updateOpponent(opponent)
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



	
