from twisted.internet import protocol,reactor
import sys
class Client():
	def __init__(self,host,port):
		self.host = host
		self.port = port
		reactor.connectTCP(self.host,self.port,CommandConnFactory())
		reactor.run()

class CommandConn(protocol.Protocol):
	def __init__(self):
		self.numMessagesReceived = 0
	def connectionMade(self):
		self.transport.write('connect')
	def dataReceived(self,data):
		if data == 'waiting for players':
			print 'Waiting for another player..'
		elif data.startsWith('PN'):
			comp = data.split(':')
			playerNumber = int(comp[1])
			print 'Game Started: You are Player',playerNumber
			gs = GameSpace(playerNumber)
			gs.main()

		self.numMessagesReceived+=1

class CommandConnFactory(protocol.ClientFactory):
	def buildProtocol(self,addr):
		return CommandConn()



	
