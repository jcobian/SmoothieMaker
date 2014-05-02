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
		self.transport.write(str(self.playerNumber)+":"+'Rect:'+pd)
		percentage = self.gs.score/float(self.gs.winningScore)
		#self.transport.write(str(self.playerNumber)+":"+'Percentage:'+str(percentage))

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
				comp = data.split(':')
				playerFrom = int(comp[0])
				objType = comp[1]
				obj = comp[2]
				if objType == 'Rect':	
					opponent = pickle.loads(obj)
					self.gs.updateOpponent(opponent)
				elif objType == 'Percentage':
					opponentPercentage = float(obj)*100
					self.gs.opponentScoreLabel.setScore(opponentPercentage)	
				self.sendMyData()
		'''
		elif data.startswith('Request'):
			comp = data.split(':')
			requestType = comp[1]
			if requestType == 'Blender':
				#print 'Received request for my blender'
				pd = pickle.dumps(self.gs.blender.rect)
				self.transport.write('Response:'+str(self.playerNumber)+':Blender:')
				#self.transport.write('Response:'+str(self.playerNumber)+':Blender:'+pd)
				print 'done pickling'
		elif data.startswith('Response'):
			comp = data.split(':')
			responseType = comp[1]
			if responseType == 'Blender':
				print 'SUCCESS, UNPICKLING HERE'
				pd = comp[2]
				opponent = pickle.loads(pd)
				self.gs.updateOpponent(opponent)
				sys.exit()
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



	
