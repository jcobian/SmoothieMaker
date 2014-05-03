from twisted.internet import protocol,reactor
from twisted.internet.task import LoopingCall
import sys
import pickle
from smoothie import GameSpace
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
	def sendMyData(self):
		pd = pickle.dumps(self.gs.blender.rect)
		score = self.gs.score
		randFruitInt = self.gs.randFruitInt
		randXPos = self.gs.randXPos
		foodType = self.gs.foodType
		randVSpeed = self.gs.randVSpeed
		valid = self.gs.shouldSendData
		if valid == 1:
			self.gs.shouldSendData = 0
		theString= str(self.playerNumber)+':'+pd+':'+str(score)+':'+str(valid)+':'+str(randFruitInt)+':'+str(randXPos)+':'+str(randVSpeed)+':'+foodType+'end'
		comp = theString.split(':')
		print 'comp send',comp
		self.transport.write(theString)
		
		
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
			self.sendMyData()
			
		else:
			self.parseData(data)
			self.sendMyData()
	def parseData(self,data):
		splitUp = data.split('end')
		for piece in splitUp:
			if len(piece)==0:
				continue

				comp = piece.split(':')
				print 'receive comp',comp
				pd = comp[1]
				opponent = pickle.loads(pd)
				self.gs.updateOpponent(opponent)
				oppScore = int(comp[2])
				self.gs.opponentScore = oppScore
				valid = int(comp[3])
				if valid == 1:
					fruitInt = int(comp[4])
					xpos = int(comp[5])
					vspeed = int(comp[6])
					foodType = comp[7]
					self.gs.addFruit(fruitInt,xpos,vspeed,foodType)

			 
		
		
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



	
