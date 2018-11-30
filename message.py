import json
from enum import Enum
import sys

DATA = "data"

SIZE_DIGITS = 4 # Length of the string representing the message size

def receiveNextMsg(conn):
    """ Receives next set of data based on prepended size information """
    """ Might need to try/catch this for closing socket"""
    try:
        msgSize = conn.recv(SIZE_DIGITS)
        rawMsg = conn.recv(int(msgSize))
        msg = Message(str = rawMsg)
        return msg
    except:
        return Message(command = Code.EXIT)


class Code(Enum):
    """ Valid message commands """
    MSG = 1      # Basic text updates
    START = 2    # Send with no data, contacts will append id
    EXIT = 3
    DATA = 4     # This will probably need to be made more specific/map seperated
    CHAR_REQ = 5 # Request a character, [name, id, charKey]
    CHAR_DENY = 6 # Rejects a character request [[available charCodes], reason]
    CHAR_ACC = 7 # Notifies of accepted character request [name, id, charCode, charName]
    WALK_REQ = 8 # Walk request [charCode, diceSum, moveStr]
    WALK_DENY = 9 # Walk rejections [reason]
    MOVE = 10    # Move notification [elemCode, (starting), (ending)]
    CARDS = 11   # [[three elemCodes]]
    ACCUSE = 12  # Accusation [name, [charCode, weaponCode, placeCode]]


class Message:
    def __init__(self, command = None, data = None, str = None):
        if str:
            try:
                dict = json.loads(str)
            except:
                print "ERROR", str
            strCommand = dict.keys()[0]
            self.command = Code(int(strCommand))
            self.data = dict[strCommand]
        else:
            self.command = command
            self.data = data

    def encode(self):
        """ Turns the message into a string + MESSAGE size
            IMPORTANT -> Message(msg.encode) will NOT work"""
        print(self.command, self.data)
        msg = json.dumps({ self.command.value : self.data})
        size = len(msg)
        strSize = "0" * (SIZE_DIGITS - len(str(size))) + str(size)
        return strSize + msg

    def pretty(self):
        """ Prints message data as """
        strPretty = ''
        if self.command in formatStrs:
            strPretty = formatStrs[self.command].format(*self.data)
        elif self.command in basicStrings:
            strPretty = basicStrings[self.command]
        elif self.command in formatFuncs:
            strPretty = formatFuncs[self.command](self.data)
        else:
            strPretty = str(self.command) + " " + str(self.data)
        return strPretty

def charDeny(data):
    list, reason = data
    lines = []
    lines.append(reason)
    lines.append("Available characters:")
    for char, suspect in list:
        lines.append('{: <35} ({})'.format(suspect, char))
    return '\n'.join(lines)

basicStrings = {
                Code.EXIT:      'Something went wrong, exiting game.'
                }

formatStrs = {  Code.START:     'Your id is {0}',
                Code.CHAR_ACC:  '{0} ({1}) has selected {3}'
             }

formatFuncs = {
                Code.CHAR_DENY: charDeny
            }
