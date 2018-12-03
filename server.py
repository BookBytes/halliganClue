#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, threading, math, sys, signal
from game import Game
from contacts import Contacts
from client_handler import ClientHandler
from message import Message, Code, receiveNextMsg

class Server(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Reference for getting host name
        # https://stackoverflow.com/questions/16130786/
        # why-am-i-getting-the-error-connection-refused-in-python-sockets
        host = socket.gethostname()
        print "The address of the host is " + host
        port = 5005
        self.s.bind((host, port))
        self.s.listen(10)
        self.number = 0
        self.lock = threading.Lock()
        # TODO: make a dictionary of connections, one sublist for each game
        self.conns = []
        signal.signal(signal.SIGINT, self.signal_handler)

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
        game = Game(len(addrList))

        self.contacts.notifyAll(Code.START)
        self.contacts.notifyAll(Code.INFO,
                            ["You wait until the fateful night of the "
                            + "party, dressing up in your finest attire. "
                            + "At the house you're greeted by a elderly "
                            + 'butler. "Which guest are you again?"'
                             + "he asks."])
        self.contacts.notifyAll(Code.CHAR_PROMPT,
                                game.availableSuspects())
                    
        for i in range(len(self.contacts)):
            threads.append(threading.Thread(target= ClientHandler.start,
                                            args=(i, game, self.contacts)))
            threads[-1].start()

        for thread in threads:
            thread.join()

        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        
    def signal_handler(obj, num, frame):
        sys.exit(0)


if __name__ == "__main__":
    s = Server()
    s.run()
