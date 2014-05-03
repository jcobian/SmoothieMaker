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
		print 'send',foodType
		self.transport.write(str(self.playerNumber)+':'+pd+':'+str(score)+':'+str(valid)+':'+str(randFruitInt)+':'+str(randXPos)+':'+str(randVSpeed)+':'+'fruit')
		'''
		myFruits = self.gs.fruits
		oppFruits = self.gs.fruitsOpp
		myDict = dict()
		fruitList = list()
		for fruit in myFruits:
			tempDict = dict()
			tempDict['image'] = fruit.fruitImage
			tempDict['frozen'] = fruit.frozen
			tempDict['rect'] = pickle.dumps(fruit.rect)
			tempDict['vspeed'] = fruit.vspeed
			tempDict['currentTicks'] = fruit.current_tick
			fruitList.append(tempDict)
		myDict['oppFruits'] = fruitList

		oppFruitList = list()
		for fruit in oppFruits:
			tempDict = dict()
			tempDict['image'] = fruit.fruitImage
			tempDict['frozen'] = fruit.frozen
			print 'in send data',fruit.rect.top
			tempDict['rect'] = pickle.dumps(fruit.rect)
			tempDict['vspeed'] = fruit.vspeed
			tempDict['currentTicks'] = fruit.current_tick
			oppFruitList.append(tempDict)

		myDict['fruits'] = oppFruitList
		pickleDict = pickle.dumps(myDict)
		self.transport.write(str(self.playerNumber)+":"+pd+':'+str(score)+':'+pickleDict)
		'''
		
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
		comp = data.split(':')
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
			self.gs.addFruit(fruitInt,xpos,vspeed,'fruit')
		'''
		pickleDict = comp[3]
		myDict = pickle.loads(pickleDict)
		self.gs.updateMyFruits(myDict['fruits'])
		self.gs.updateOppFruits(myDict['oppFruits'])
		'''
		


	


class CommandConnFactory(protocol.ClientFactory):
	def __init__(self,client):
		self.client = client
	def buildProtocol(self,addr):
		return CommandConn(self.client)

if __name__ == '__main__':
	host = sys.argv[1]
	port = int(sys.argv[2])
	client = Client(host,port)



	
