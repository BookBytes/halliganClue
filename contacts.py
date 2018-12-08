from message import Message, Code

class Contacts:
    def __init__(self):
        self.contacts = {}
        self.order = []
        self.first = 0

    def add(self, connection):
        """ Adds a connection, eventually this will need to be altered
        to account for order and such. For now id = insertion order. """
        id = len(self.contacts)
        self.contacts[id] = connection
        self.order.append(id)

    def notify(self, id, command, data = None):
        """ Notifies the connection with the given id """
        print "sending:", id, command, data
        if command == Code.START: data = [id]
        try:
            msg = Message(command = command, data = data)
            self.contacts[id].send(msg.encode())
        except:
            print "msg failed"

    def nextTurnId(self, id):
        # Does not return removed players
        index = self.order.index(id)
        return self.order[ (index + 1) % len(self.order) ]


    def nextPlayerId(self, id):
        # Returns removed players
        return (id + 1) % len(self.contacts)

    def remove(self, id):
        #Returns true if no more players
        self.order.remove(id)
        return len(self.order) == 0

    def notifyAll(self, command, data = None):
        """ Notifies all connections """
        for id in self.contacts:
            self.notify(id, command, data)

    def __len__(self):
        return len(self.contacts)

    def __getitem__(self, i):
        return self.contacts[i]
