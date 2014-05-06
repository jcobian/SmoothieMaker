#Jonathan Cobian and Oliver Lamb
#CSE 30331
#Server for our Smoothie Maker game
from twisted.internet import protocol, reactor
from twisted.internet.defer import DeferredQueue
from twisted.protocols.basic import LineReceiver
import random
import sys
class Server():
	def __init__(self,fruitPort,blenderPort):
		#list of connections
		self.fruitConns = list()
		self.blenderConns = list()
		self.freezeConns = list()
		self.randSeed = 0
		print 'Waiting for connections..'
		reactor.listenTCP(fruitPort,FruitConnFactory(self))
		reactor.listenTCP(blenderPort,BlenderConnFactory(self))
		reactor.run()
	#add player to your list of connections and return the player number
	def addFruitConn(self,fruitConn):
		if len(self.fruitConns) == 2:
			print 'ERROR: MORE THAN TWO PLAYERS, THIS FEATURE NOT ESTABLISHED YET'
			sys.exit()
		self.fruitConns.append(fruitConn)
		return len(self.fruitConns)
	def addBlenderConn(self,conn):
		self.blenderConns.append(conn)
		return len(self.blenderConns)
	def addFreezeConn(self,conn):
		self.freezeConns.append(conn)
		return len(self.freezeConns)
	#returns true if 2 players are connected, false o/w
	def isReadyToPlay(self):
		if len(self.fruitConns) == 2:
			random.seed()
			self.randSeed = random.randint(0,100)
			return True
		return False
	def lostConn(self):
		for conn in self.fruitConns:
			conn.sendLine('lost conn')
			conn.transport.loseConnection()
		for conn in self.blenderConns:
			conn.transport.loseConnection()
		del self.fruitConns[:]
		del self.blenderConns[:]
		print 'Game Ended because of a loss of a connection'
		print 'Ready for new game'
		print 'Waiting for connections...'
	def startGame(self):
		for conn in self.fruitConns:
			conn.givePlayerNumber()	

class BlenderConn(protocol.Protocol):
	def __init__(self,server):
		self.server = server #get a reference to the server
		#get your plyaer number
		playerNumber = self.server.addBlenderConn(self)
		self.playerNumber = playerNumber
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.handleData)
	def connectionLost(self,reason):
		print 'Lost connection with player',self.playerNumber
		self.server.lostConn()
	#just forward the data on to the other client
	def handleData(self,data):
		comp = data.split(':')
		playerFrom = int(comp[0])
		playerTo = 0
		if playerFrom == 1:
			playerTo = 1
		elif playerFrom == 2:
			playerTo=0
		self.server.blenderConns[playerTo].transport.write(data)
		self.queue.get().addCallback(self.handleData)
	def dataReceived(self,data):
		self.queue.put(data)

class FruitConn(LineReceiver):
	def __init__(self,server):
		self.server = server #get a reference to the server
		#get your plyaer number
		playerNumber = self.server.addFruitConn(self)
		self.playerNumber = playerNumber
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.handleData)
		print 'Player ',str(self.playerNumber),' connected'
	def connectionLost(self,reason):
		print 'Lost connection with player',self.playerNumber
		self.server.lostConn()
	#happens once per game, gives the player his player number and the random seed to both palyers make the same fruits
	def givePlayerNumber(self):
		self.sendLine('PN:'+str(self.playerNumber)+':'+str(self.server.randSeed))
	#just forward the data on to the other client
	def handleData(self,data):
		comp = data.split(':')
		playerFrom = int(comp[0])
		playerTo = 0
		if playerFrom == 1:
			playerTo = 1
		elif playerFrom == 2:
			playerTo=0
		self.server.fruitConns[playerTo].sendLine(data)
		self.queue.get().addCallback(self.handleData)
	def lineReceived(self,data):
		if data == 'start':
			if self.server.isReadyToPlay():
				self.server.startGame()
			else:
				self.sendLine('waiting for players')
		else:
			self.queue.put(data)
					
class BlenderConnFactory(protocol.Factory):
	def __init__(self,server):
		self.server = server
	def buildProtocol(self,addr):
		blenderConn = BlenderConn(self.server)
		return blenderConn 


class FruitConnFactory(protocol.Factory):
	def __init__(self,server):
		self.server = server
	def buildProtocol(self,addr):
		fruitConn = FruitConn(self.server)
		return fruitConn

if __name__ == '__main__':
	fruitPort = int(sys.argv[1])
	blenderPort = int(sys.argv[2])
	server = Server(fruitPort,blenderPort)
