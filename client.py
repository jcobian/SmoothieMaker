from twisted.internet import protocol,reactor
import sys
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
			playerNumber = int(comp[1])
			print 'Game Started: You are Player',playerNumber
			gs = GameSpace(self,playerNumber)
			gs.main()
			lc = LoopingCall(gs.gameLoopIteration)
			lc.start(1/60)
		elif data == 'Response:Blender':
			pass

	def getOpponentBlender(self):
		self.transport.write('Request:Blender')


class CommandConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return CommandConn(self.client)

if __name__ == '__main__':
	host = sys.argv[1]
	port = int(sys.argv[2])
	client = Client(host,port)



	
