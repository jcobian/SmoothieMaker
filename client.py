from twisted.internet import protocol,reactor
from twisted.internet.task import LoopingCall
import sys
import pickle
from smoothie import GameSpace
from twisted.internet.defer import DeferredQueue
class Client():
	def __init__(self,host,port):
		self.host = host
		self.port = port
		reactor.connectTCP(self.host,self.port,CommandConnFactory(self))
		reactor.run()


class CommandConn(protocol.Protocol):
	def __init__(self,client):
		self.numMessagesReceived = 0
		self.client = client
		self.fruitQueue = DeferredQueue()
		self.fruitQueue.get().addCallback(self.sendMyData)


	def sendMyData(self,fruitData):
		pd = pickle.dumps(self.gs.blender.rect)
		score = self.gs.score
		datapd =  pickle.dumps(fruitData)
		'''
		randFruitInt = fruitData.fruitInt
		randXPos = fruitData.xpos
		foodType = fruitData.fruitType
		randVSpeed = fruitData.vspeed
		'''
		'''
		randFruitInt = self.gs.randFruitInt
		randXPos = self.gs.randXPos
		foodType = self.gs.foodType
		randVSpeed = self.gs.randVSpeed
		'''
		theString = str(self.playerNumber)+':'+pd+':'+str(score)+':'+datapd
		#theString= str(self.playerNumber)+':'+pd+':'+str(score)+':'+str(randFruitInt)+':'+str(randXPos)+':'+str(randVSpeed)+':'+foodType+'end'
		comp = theString.split(':')
		self.transport.write(theString)

	def readyForMore(self):
		self.fruitQueue.get().addCallback(self.sendMyData)


		
		
	def closeConn(self):
		reactor.stop()
	def connectionMade(self):
		self.transport.write('connect')
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
			#IS THIS NEEDED
			#self.sendMyData()
		elif data == 'ready for more':
			self.readyForMore()
			
		else:
			self.parseData(data)
			#self.sendMyData()
	def parseData(self,data):
		comp = data.split(':')
		pd = comp[1]
		opponent = pickle.loads(pd)
		self.gs.updateOpponent(opponent)
		oppScore = int(comp[2])
		self.gs.opponentScore = oppScore
		fruitData = pickle.loads(comp[3])
		self.gs.addFruit(fruitData.fruitInt,fruitData.xpos,fruitData.vspeed,fruitData.foodType)
		self.transport.write('added fruit:'+str(self.playerNumber))


		'''
		splitUp = data.split('end')
		for piece in splitUp:
			if len(piece)==0:
				continue
			comp = piece.split(':')
			pd = comp[1]
			opponent = pickle.loads(pd)
			self.gs.updateOpponent(opponent)
			oppScore = int(comp[2])
			self.gs.opponentScore = oppScore
			valid = int(comp[3])
			print 'valid is ',valid
			if valid == 1:
				fruitInt = int(comp[4])
				xpos = int(comp[5])
				vspeed = int(comp[6])
				foodType = comp[7]
				print self.playerNumber,'is adding:',fruitInt,xpos,vspeed,foodType
				self.gs.addFruit(fruitInt,xpos,vspeed,foodType)
		'''

			 
		
		
	def gameOver(self,text):
		self.lc = LoopingCall(self.gs.goToGameOver,(text))
		self.lc.start(1/60)

	


class CommandConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return CommandConn(self.client)

if __name__ == '__main__':
	host = sys.argv[1]
	port = int(sys.argv[2])
	client = Client(host,port)



	
