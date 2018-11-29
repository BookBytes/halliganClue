#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from game import Game


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

    def handle_client(self, addr, conn, data):
        # send character name followed by the map
        conn.send("You're playing as " + data[0] + ".")
        conn.send(data[1])
        while 1:
            inData = conn.recv(20)
            if not inData:
                break
            print "received data:", inData
            # TODO: act based on message format; call appropriate function
            # conn.send("Success") # send success or failure message
            for connection in self.conns:
                connection.send(data[1])  # broadcast the updated board to all clients
        conn.close()

    def run(self):
        addrToGame = {}
        addrList = []

        while 1:
            while self.number < 3:
                incomingConn, incomingAddr = self.s.accept()
                if incomingAddr not in addrToGame:
                    self.conns.append(incomingConn)
                    addrList.append(incomingAddr)
                    addrToGame[incomingAddr] = 1
                    self.number += 1
                    print 'Connection address:', incomingAddr
            for conn in self.conns:
                conn.send('Game can start now!')
            break

        self.initiateGame(addrList)

    def initiateGame(self, addrList):
        threads = []
        game = Game(addrList)

        for i in range(len(self.conns)):
            threads.append(threading.Thread(target=self.handle_client,
                                            args=(addrList[i],
                                                  self.conns[i],
                                                  [game.getChar(addrList[i]), game.map])))
            threads[-1].start()

        for thread in threads:
            thread.join()
