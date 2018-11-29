import json
from enum import Enum
import sys

DATA = "data"

SIZE_DIGITS = 4 # Length of the string representing the message size

def receive_next(conn):
    """ Receives next set of data based on prepended size information """
    msg_size = conn.recv(SIZE_DIGITS)
    raw_msg = conn.recv(int(msg_size))
    return raw_msg


class Code(Enum):
    """ Valid message commands """
    MSG = 1   # Basic text updates
    START = 2
    LEAVE = 3
    DATA = 4  # This will probably need to be made more specific/map seperated
    CHAR_REQ = 5 # Request a character, [name, char_code]
    CHAR_REJ = 6 # Rejects a character request [[available char_codes]]
    CHAR_ACC = 7 # Notifies of accepted character request [name, char_code]
    WALK_REQ = 8 # Walk request [char_code, move_str]
    WALK_REJ = 9 # Walk rejections [reason]
    MOVE = 10    # Move notification [elem_code, (starting), (ending)]
    DECK = 11    # [[three elem_codes]]


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
        str_size = "0" * (SIZE_DIGITS - len(str(size))) + str(size)
        return str_size + msg

    def toString(self):
        """ Pretty print message)"""
        # TODO: actually format nice strings
        return self.encode()

    def get_command(self):
        """ Get Code instance of command """
        return self.command

    def get_data(self):
        """ Get body data """
        return self.data
