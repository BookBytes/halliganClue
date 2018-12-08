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
        self.number = -1
        self.maxPlayers = 2
        self.maxSessions = 10
        self.lock = threading.Lock()
        # A dictionary of connections, one sublist for each game
        self.conns = []
        signal.signal(signal.SIGINT, self.signal_handler)

    def run(self):
        addrToGame = {}
        #contacts = Contacts()
        contacts = []
        addrList = []
        sessions = []

        while 1:
            if self.number == -1:
                print 'Game ' + str(len(self.conns))
                session = threading.Thread(target= self.initiateGame,
                                           args= [addrList, contacts])
                sessions.append(session)
                self.number += 1
                #contacts = Contacts()  
            if len(sessions) > self.maxSessions:
                del sessions[0]
            while self.number < self.maxPlayers:
                incomingConn, incomingAddr = self.s.accept()
                if incomingAddr not in addrToGame:
                    #contacts.add(incomingConn)
                    contacts.append(incomingConn)
                    addrList.append(incomingAddr)
                    addrToGame[incomingAddr] = 1
                    self.number += 1
                    print '>>> Connection address:', incomingAddr
            #break
            self.conns.append(addrList)
            session.start()
            addrList = []
            contacts = []
            self.number = -1

        for session in sessions:
            session.join()
            #self.initiateGame(addrList)

    def initiateGame(self, addrList, contactList):
        print addrList
        threads = []
        game = Game(len(addrList))
        contacts = Contacts()
        for con in contactList:
            contacts.add(con)

        contacts.notifyAll(Code.START)
        contacts.notifyAll(Code.INFO,
                            ["You wait until the fateful night of the "
                            + "party, dressing up in your finest attire. "
                            + "At the house you're greeted by a elderly "
                            + 'butler. "Which guest are you again?"'
                             + "he asks."])
        contacts.notifyAll(Code.CHAR_PROMPT,
                                game.availableSuspects())

        for i in range(len(contacts)):
            threads.append(threading.Thread(target= ClientHandler.start,
                                            args=(i, game, contacts)))
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
