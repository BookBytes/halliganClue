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

    def handle_client(self, addr, conn, data):
        # TODO - send character data
        # send map
        conn.send(data)
        while 1:
            data = conn.recv(20)
            if not data:
                break
            print "received data:", data
            conn.send(data)
        conn.close()

    def run(self):
        addrToGame = {}
        conns = []
        addrList = []

        while 1:
            while self.number < 3:
                incomingConn, incomingAddr = self.s.accept()
                if incomingAddr not in addrToGame:
                    conns.append(incomingConn)
                    addrList.append(incomingAddr)
                    addrToGame[incomingAddr] = 1
                    self.number += 1
                    print 'Connection address:', incomingAddr
            for conn in conns:
                conn.send('Game can start now!')
            break

        self.initiateGame(conns, addrList)

    def initiateGame(self, conns, addrList):
        threads = []
        game = Game(addrList)

        for i in range(len(conns)):
            threads.append(threading.Thread(target=self.handle_client,
                                            args=(addrList[i], conns[i], game.map)))
            threads[-1].start()

        for thread in threads:
            thread.join()
