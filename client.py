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
		pass
	def connectionMade(self):
		print 'yay'
		self.transport.write('connection made')
	def dataReceived(self,data):
		print ' got data'

class CommandConnFactory(protocol.ClientFactory):
	def buildProtocol(self,addr):
		return CommandConn()



	
