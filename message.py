import json

JOIN = "join"
LEAVE = "leave"

class Message:
    def __init__(self, command, data):
        self.command = command
        self.data = data

    @classmethod
    def decode(self, str):
        """ Converts raw message data back to message object """
        return self()

    def encode(self):
        return json.dumps({self.command : self.data})

    def toString(self):
        """ Pretty print message """
        return self.encode()
