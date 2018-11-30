from message import Message

class Contacts:
    def __init__(self):
        self.contacts = {}

    def add(self, connection):
        """ Adds a connection, eventually this will need to be altered
        to account for order and such. For now id = insertion order. """
        self.contacts[len(self.contacts)] = connection

    def notify(self, id, command, data = None):
        """ Notifies the connection with the given id """
        print "sending:", id, command, data
        try:
            msg = Message(command = command, data = data)
            self.contacts[id].send(msg.encode())
        except:
            print "msg failed"

    def notifyNext(self, id, command, data = None):
        """ Notifies next connection in order """
        next = (id + 1) % len(self)
        self.notify(next, command, data)

    def notifyAll(self, command, data = None):
        """ Notifies all connections """
        for id in self.contacts:
            self.notify(id, command, data)

    def __len__(self):
        return len(self.contacts)

    def __getitem__(self, i):
        return self.contacts[i]
