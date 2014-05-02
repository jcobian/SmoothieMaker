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
		self.transport.write(str(self.playerNumber)+":"+pd+':'+str(score))
		

	def connectionMade(self):
		self.transport.write('connect')
	def dataReceived(self,data):
		if data == 'waiting for players':
			print 'Waiting for another player..'
		elif data.startswith('PN'):
			comp = data.split(':')
			self.playerNumber = int(comp[1])
			print 'Game Started: You are Player',self.playerNumber
			self.gs = GameSpace(self,self.playerNumber)
			self.gs.main()
			lc = LoopingCall(self.gs.gameLoopIteration)
			lc.start(1/60)
			self.sendMyData()
			
		else:
			self.parseData(data)
			self.sendMyData()
	def parseData(self,data):
		comp = data.split(':')
		pd = comp[1]
		opponent = pickle.loads(pd)
		self.gs.updateOpponent(opponent)
		oppScore = int(comp[2])
		self.gs.opponentScore = oppScore


	


class CommandConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return CommandConn(self.client)

if __name__ == '__main__':
	host = sys.argv[1]
	port = int(sys.argv[2])
	client = Client(host,port)



	
