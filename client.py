#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, threading, time, sys, signal
from message import Message, Code, receiveNextMsg, stringifyDict

class Client(object):
    # Initiate the client with character and cards
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.handleMsgCode = { Code.EXIT:      self.leave,
                            Code.CHAR_PROMPT:  self.charPrompt,
                            Code.CHAR_ACC:     self.charAccept,
                            Code.INFO:         self.printData,
                            Code.MAP:          self.printMap,
                            Code.DECK:         self.receiveDeck,
                            Code.TURN_PROMPT:  self.turnPrompt,
                            Code.MOVE_PROMPT:  self.movePrompt,
                            Code.ACC_PROMPT:   self.accusePrompt,
                            Code.SUG_PROMPT:   self.suggestionPrompt,
                            Code.TURN_CONT:    self.turnPrompt,
                            Code.SUGGESTION:   self.evalSuggestion }
        signal.signal(signal.SIGINT, self.signal_handler)

    def run(self):
        host = raw_input("Welcome, you've been invited for a formal dinner "
                    + "at the house of Dr. Fisher to celebrate the end "
                    + "of the semester. Please enter your host's address: ")
        port = 5005
        self.s.connect((host, port))
        self.waitToStart()

    def waitToStart(self):
        self.name = raw_input("Confirm your name on the guest list: ")

        self.send(Code.NAME, [self.name])

        msg = receiveNextMsg(self.s)
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

    def signal_handler(obj, num, frame):
        sys.exit(0)


##############################################################################
### Code for handling each message code
### Arguments
###        self
###        data - data from message packet
##############################################################################
    def printData(self, data):
        pass

    def printMap(self, map):
        pass

    def receiveDeck(self, data):
        self.deck = data

    def leave(self, _data ):
        self.s.close()
        exit()

    def charPrompt(self, _data):
        character = raw_input("Character symbol:")
        self.send(Code.CHAR_REQ, [character])

    def charAccept(self, data):
        name, id, charCode, charName = data
        if id == self.id:
            self.charCode = charCode

    def turnPrompt(self, data):
        options = data
        action = raw_input("What action will you take? : ")
        self.send(Code.TURN, [action, options ])

    def movePrompt(self, data):
        [diceRoll] = data
        movement = raw_input("")
        self.send(Code.MOVE, [diceRoll, movement])

    def accusePrompt(self, _data):
        murderer = raw_input("Murderer: ")
        weapon = raw_input("Weapon: ")
        location = raw_input("Location: ")
        self.send(Code.ACCUSE, [murderer, weapon, location])

    def suggestionPrompt(self, _data):
        murderer = raw_input("Murderer: ")
        weapon = raw_input("Weapon: ")
        location = raw_input("Location: ")
        self.send(Code.SUGGESTION, [self.id, [murderer, weapon, location]])

    def evalSuggestion(self, data):
        id, keys = data
        inDeck = {}
        raw_input("Press any key to view your hand...")
        for cardKey in self.deck:
            if cardKey in keys:
                inDeck[cardKey] = self.deck[cardKey]
        if len(inDeck):
            print stringifyDict("", inDeck)
            showKey = raw_input("Which will you show?:")
            self.send(Code.CARD_SHOW, [id, showKey, inDeck, keys])

        else:
            print "You have none of these cards"
            raw_input("Press any key to pass...")
            self.send(Code.CARD_SHOW, [id, None, [], keys])


##############################################################################

if __name__ == "__main__":
    c = Client()
    c.run()
