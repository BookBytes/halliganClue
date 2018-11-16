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
		self.s.connect(('127.0.0.1', 5005))
	def send(self, MESSAGE):
		self.s.send(MESSAGE)
	def receive(self):
		data =  self.s.recv(1024)
		print "received data:", data
	def close(self):
		self.s.close()

class Server(object):
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind(('127.0.0.1', 5005))
		self.s.listen(10)

	def handle_client(self, addr, conn):
		while 1:
			data = conn.recv(20)
			if not data: break
			print "received data:", data
			conn.send(data)
		conn.close()

	def run(self):
		thread = []
		addr = {}
		while 1:
			conn1, addr1 = self.s.accept()
			if addr1 not in addr:
				addr[addr1] = 1
				print 'Connection address:', addr1
				thread.append(threading.Thread(target = self.handle_client,\
				 args = (addr1,conn1)))
				thread[-1].start()

