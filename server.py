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


    def handleClient(self, addr, id_self, game):
        conn_self = self.contacts[id_self]

        # TODO - send character data
        # send map
        #self.contacts.notify(id_self, Code.DATA, data)

        while 1:
            msg = receiveNextMsg( conn_self )
            print "received data:", msg.command, msg.data
            if msg.command == Code.CHAR_REQ:
                name, char_code = msg.data
                success, reason = game.claim_suspect(char_code)
                if success:
                    self.contacts.notifyAll(Code.CHAR_ACC, [name, char_code])
                else:
                    self.contacts.notify(   id_self,
                                            Code.CHAR_DENY,
                                            [ game.available_suspects(),
                                             reason ])
            elif msg.command == Code.EXIT:
                self.contacts.notifyAll(Code.EXIT)
                #self.s.shutdown(socket.SHUT_RDWR)
                #self.s.close()

            else:
                self.contacts.notifyAll(Code.DATA, msg.data)

        conn_self.close()

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
                                [game.available_suspects(),
                                "Please select a character"])

        for i in range(len(self.contacts)):
            threads.append(threading.Thread(target=self.handleClient,
                                            args=(addrList[i], i, game)))
            threads[-1].start()

        for thread in threads:
            thread.join()
