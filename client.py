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
			lc = LoopingCall(gs.gameLoopIteration)
			lc.start(1/60)
		elif data.startswith('Request');
			comp = data.split(':')
			requestType = comp[1]
			if requestType == 'Blender':
				pd = pickle.dumps(self.gs.blender)
				self.transport.write('Response:'+str(self.playerNumber)+':Blender:'+pd)
		elif data.startswith('Response'):
			comp = data.split(':')
			responseType = comp[1]
			if responseType == 'Blender':
				pd = comp[2]
				opponent = pickle.loads(pd)
				gs.updateOpponent(opponent)

	def getOpponentBlender(self):
		self.transport.write('Request:'+str(self.playerNumber)+':Blender')


class CommandConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return CommandConn(self.client)

if __name__ == '__main__':
	host = sys.argv[1]
	port = int(sys.argv[2])
	client = Client(host,port)



	
