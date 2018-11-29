#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from game import Game
from message import Message, Code, receive_next
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


    def handle_client(self, addr, id_self, data):
        conn_self = self.contacts[id_self]

        # TODO - send character data
        # send map
        self.contacts.notify(id_self, Code.DATA, data)

        while 1:
            data = receive_next( conn_self )
            if not data:
                break
            print "received data:", data
            self.contacts.notifyAll(Code.DATA, data)

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
            self.contacts.notifyAll(Code.START)
            break

        self.initiateGame(addrList)

    def initiateGame(self, addrList):
        threads = []
        game = Game()

        for i in range(len(self.contacts)):
            threads.append(threading.Thread(target=self.handle_client,
                                            args=(addrList[i], i, game.map)))
            threads[-1].start()

        for thread in threads:
            thread.join()
