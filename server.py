#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from game import Game
from message import Message, Code, receiveNextMsg
import math
from contacts import Contacts


class Server(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 5005))
        self.s.listen(10)
        self.number = 0
        self.lock = threading.Lock()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # TODO: make a dictionary of connections, one sublist for each game
        self.conns = []


    def handleClient(self, addr, idSelf, game):
        connSelf = self.contacts[idSelf]

        # TODO - send character data
        # send map
        #self.contacts.notify(idSelf, Code.DATA, data)

        while 1:
            msg = receiveNextMsg( connSelf )
            print "received data:", msg.command, msg.data
            if msg.command == Code.CHAR_REQ:
                name, id, charKey = msg.data
                char, reason = game.claimSuspect(charKey)
                if char:
                    self.contacts.notifyAll(Code.CHAR_ACC,
                                            [name, id, char.name, char.value])
                else:
                    self.contacts.notify(   idSelf,
                                            Code.CHAR_DENY,
                                            [ game.availableSuspects(),
                                             reason ])
            elif msg.command == Code.EXIT:
                self.contacts.notifyAll(Code.EXIT)
                #self.s.shutdown(socket.SHUT_RDWR) # -> Bad file descriptor
                self.s.close()
                break

            else:
                self.contacts.notifyAll(Code.DATA, msg.data)

        connSelf.close()

    def run(self):
        addrToGame = {}
        self.contacts = Contacts()
        addrList = []

        while 1:
            while self.number < 3:
                incomingConn, incomingAddr = self.s.accept()
                if incomingAddr not in addrToGame:
                    self.contacts.add(incomingConn)
                    addrList.append(incomingAddr)
                    addrToGame[incomingAddr] = 1
                    self.number += 1
                    print 'Connection address:', incomingAddr
            break

        self.initiateGame(addrList)

    def initiateGame(self, addrList):
        threads = []
        game = Game(addrList)

        self.contacts.notifyAll(Code.START)
        self.contacts.notifyAll(Code.CHAR_DENY,
                                [game.availableSuspects(),
                                "Please select a character"])

        for i in range(len(self.contacts)):
            threads.append(threading.Thread(target=self.handleClient,
                                            args=(addrList[i], i, game)))
            threads[-1].start()

        for thread in threads:
            thread.join()
