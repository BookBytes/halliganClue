#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from message import Message, Code, receiveNextMsg
import time
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

        self.handleMsgCode = { Code.EXIT:      self.leave,
                            Code.CHAR_PROMPT:  self.charPrompt,
                            Code.CHAR_ACC:     self.charAccept,
                            Code.INFO:         self.printData,
                            Code.MAP:          self.printMap,
                            Code.DECK:         self.printData,
                            Code.TURN_PROMPT:  self.turnPrompt,
                            Code.MOVE_PROMPT:  self.movePrompt,
                            Code.ACC_PROMPT:   self.accusePrompt }

    def run(self):
        self.s.connect(('127.0.0.1', 5005))
        self.waitToStart()

    def waitToStart(self):
        self.name = raw_input("What's your name:")

        self.send(Code.NAME, [self.name])

        msg = receiveNextMsg(self.s)
        # Might want to drop this out or have a count down or something?
        while msg.command != Code.START:
            msg = receiveNextMsg(self.s)
        [self.id] = msg.data
        print msg.pretty()
        self.startGame()


    def startGame(self):
        self.gameInProgress = True

        while self.gameInProgress:
            msg = receiveNextMsg(self.s)
            print "--------------------------------------"
            print msg.pretty()
            if msg.command in self.handleMsgCode:
                self.handleMsgCode[msg.command](msg.data)
            else:
                pass



    # Send message to server
    def send(self, command, data = None):
        msg = Message(command = command, data = data)
        self.s.send( msg.encode() )


##############################################################################
### Code for handling each message code
### Arguments
###        self
###        data - data from message packet
##############################################################################
    def printData(self, data):
        #print data
        pass

    def printMap(self, map):
        #print map
        pass

    def leave(self, _data ):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        exit()

    def charPrompt(self, data):
        character = raw_input("Character symbol:")
        self.send(Code.CHAR_REQ, [character])

    def charAccept(self, data):
        name, id, charCode, charName = data
        if id == self.id:
            self.charCode = charCode

    def turnPrompt(self, data):
        options, reason = data
        action = raw_input("What action will you take? : ")
        self.send(Code.TURN, [action, options.keys() ])

    def movePrompt(self, data):
        diceRoll, reason = data
        movement = raw_input("")
        self.send(Code.MOVE, [diceRoll, movement])

    def accusePrompt(self, data):
        [reason] = data
        murderer = raw_input("Murderer: ")
        weapon = raw_input("Weapon: ")
        location = raw_input("Location: ")
        self.send(Code.ACCUSE, [murderer, weapon, location])


##############################################################################

if __name__ == "__main__":
    c = Client()
    c.run()
