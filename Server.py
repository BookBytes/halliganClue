import socket
import threading


class Server(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 5005))
        self.s.listen(10)
        self.number = 0
        self.lock = threading.Lock()

    def handle_client(self, addr, conn):
        while 1:
            data = conn.recv(20)
            if not data:
                break
            print "received data:", data
            conn.send(data)
        conn.close()

    def run(self):
        thread = []
        addr = {}
        conn = []
        addr2 = []
        while 1:
            while self.number < 3:
                conn1, addr1 = self.s.accept()
                if addr1 not in addr:
                    conn.append(conn1)
                    addr2.append(addr1)
                    addr[addr1] = 1
                    self.number += 1
                    print 'Connection address:', addr1
            for conn1 in conn:
                conn1.send('Game can start now!')
            break
        for i in range(len(conn)):
            thread.append(threading.Thread(target = self.handle_client,
                                           args = (addr2[i],conn[i])))
            thread[-1].start()
