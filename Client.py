import socket
import threading
# The following file is client_server model.
# How to run my program:
# Open different tabs in terminal, one terminal can run server code
# the other run clients code.

# Run server: initialize a Server with b = Server(), then type
# b.run() to run the server. After that, the server will receive
# message from client, print it on the screen and return to the client

# Run client: initialize a Client with a = Client(), then start to
# send message and receive message. close() if you want to terminate
# the client


class Client(object):
	# Initiate the client with character and cards
	def __init__(self, name, cards):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.character = name
		self.cards = cards
	# Run the client
	def run(self):
		self.s.connect(('127.0.0.1', 5005))
		while 1:
			data = self.s.recv(1024)
			print data
			break
	# Send message to the server
	def send(self, MESSAGE):
		self.s.send(MESSAGE)
	# Receive message from server and print out the message
	def receive(self):
		data =  self.s.recv(1024)
		print "received data:", data
	# Leave the room an notify the server
	def leave(self):
		self.send(self.character + " leave the room")
		self.s.close()
	# Request the element
	def request_element(self, element):
		self.send(self.character + " request " + element)
	# Request map from the server
	def request_map(self):
		self.send(self.character + " request " + map)