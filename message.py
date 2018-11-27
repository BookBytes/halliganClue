import json
from enum import Enum
import sys

HAS_MORE = "more"
DATA = "data"

CHUNK_SIZE = 900 # + _ for total size??? Gotta keep total msg size <1024

class Code(Enum):
    JOIN = 1
    START = 2
    LEAVE = 3
    DATA = 4

class Message:
    def __init__(self, command = None, data = None, hasMore = False, str = None):
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
            self.data = {DATA: data, HAS_MORE: hasMore}

    def encode(self):
        """ Turns the message into a string """
        msg = json.dumps({ self.command.value : self.data})
        print "size of message", sys.getsizeof(msg)
        return msg

    def toString(self):
        """ Pretty print message)"""
        # TODO: actually format nice strings
        return self.encode()

    def get_command(self):
        # Get Code instance of command
        return self.command

    def get_data(self):
        # Get body data
        return self.data[DATA]

    def has_more_data():
        # Check is more data is following this message
        return self.data[HAS_MORE]
