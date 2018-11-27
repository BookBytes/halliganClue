#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from game import Game
from message import Message, Code, CHUNK_SIZE
import math

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
        self.send(conn,Code.DATA, data)
        while 1:
            data = conn.recv(20)
            if not data:
                break
            print "received data:", data
            self.send(conn, Code.DATA, data)
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
                self.send(conn, Code.START)
            break

        self.initiateGame(conns, addrList)

    def send(self, conn, command, data = None):
        """ Sends a message to the specified connection address, breaks data
            into chunks if needed. """
        if data:
            chunks = int(math.ceil(float(len(data))/CHUNK_SIZE))
            print "chunks are", chunks
            data_chunk = [ data[i : i + CHUNK_SIZE] 
                            for i in range(0, len(data), CHUNK_SIZE) ]
            print "data chunks are", data_chunk
            for i in range(0, chunks):
                print "i is", i
                hasMore = False if i == (chunks - 1) else True
                conn.send(Message(  command     = command,
                                    data        = data_chunk[i],
                                    hasMore     = hasMore).encode())
        else:
            conn.send(Message(command = command).encode())

    def initiateGame(self, conns, addrList):
        threads = []
        game = Game()

        for i in range(len(conns)):
            threads.append(threading.Thread(target=self.handle_client,
                                            args=(addrList[i], conns[i], game.map)))
            threads[-1].start()

        for thread in threads:
            thread.join()
