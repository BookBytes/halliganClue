import json
from enum import Enum
import sys

DATA = "data"

MSG_SIZE = 1024
CHUNK_SIZE = 900 # For breaking up data, keep total msg size <1024

class Code(Enum):
    JOIN = 1
    START = 2
    LEAVE = 3
    DATA = 4

class Message:
    def __init__(self, command = None, data = None, str = None):
        if str:
            try:
                dict = json.loads(str)
            except:
                print "ERROR", str
            str_command = dict.keys()[0]
            self.command = Code(int(str_command))
            self.data = dict[str_command]
        else:
            self.command = command
            self.data = data

    def encode(self):
        """ Turns the message into a string + MESSAGE size
            IMPORTANT -> Message(msg.encode) will NOT work"""
        msg = json.dumps({ self.command.value : self.data})
        size = len(msg)
        str_size = "0" * (4 - len(str(size))) + str(size)
        print "size of message",
        return str_size + msg

    def toString(self):
        """ Pretty print message)"""
        # TODO: actually format nice strings
        return self.encode()

    def get_command(self):
        # Get Code instance of command
        return self.command

    def get_data(self):
        # Get body data
        return self.data
