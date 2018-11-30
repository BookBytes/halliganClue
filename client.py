#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from message import Message, Code, receiveNextMsg
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
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#io_lock = threading.Lock()
		#receiver = threading.Thread(target=receive, args = (io_lock))
		#intera
	def run(self):
		self.s.connect(('127.0.0.1', 5005))

		self.waitToStart()

	def waitToStart(self):
		self.name = raw_input("What's your name:")
		self.send(Code.DATA, self.name)
		msg = None

		# Might want to drop this out or have a count down or something?
		while msg and msg.command != Code.START:
			msg = receiveNextMsg(self.s)
			print "Received:"
			print msg.command
			data = msg.data
			print data
			print "------"

		self.startGame()

	def startGame(self):
		while True:
			msg = receiveNextMsg(self.s)
			if msg.command == Code.CHAR_DENY:
				print "Available characters", msg.data
				character = raw_input("What character:")
				self.send(Code.CHAR_REQ, [self.name, character])
			elif msg.command == Code.CHAR_ACC:
				if msg.data[0] == self.name:
					self.character = character
			elif msg.command == Code.EXIT:
				print "Something went wrong, exiting game."
				self.s.shutdown(socket.SHUT_RDWR)
				self.s.close()
				break
			print "Received:"
			print msg.command
			data = msg.data
			print data
			print "------"


	# Send message to server
	def send(self, command, data = None):
		msg = Message(command = command, data = data)
		self.s.send( msg.encode() )

	# # Leave the room and notify the server
	# def leave(self):
	# 	leave = Message(self.character + " leave the room", "")
	# 	self.send(leave)
	# 	self.s.close()
	# # Request the element
	# def request_element(self, element):
	# 	send = Message(self.character + " request " + element, "")
	# 	self.send(send)
	# # Request map from the server
	# def request_map(self):
	# 	self.send(self.character + " request map")



if __name__ == "__main__":
	c = Client()
