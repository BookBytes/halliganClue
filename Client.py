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
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def send(self, MESSAGE):
		self.s.send(MESSAGE)
	def receive(self):
		data =  self.s.recv(1024)
		print "received data:", data
	def run(self):
		self.s.connect(('127.0.0.1', 5005))
		while 1:
			data = self.s.recv(1024)
			print data
			break
	def close(self):
		self.s.close()