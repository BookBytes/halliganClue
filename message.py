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
    NAME = 1         # Sends player name to server
    START = 2        # Send with no data, contacts will append id
    EXIT = 3
    DATA = 4         # This is for misc. data BESIDES map
    CHAR_REQ = 5     # Request a character, [charKey]
    CHAR_PROMPT = 6  # Rejects a character request [[available charCodes], reason]
    CHAR_ACC = 7     # Notifies of accepted character request [name, id, charCode, charName]
    CARDS = 8        # [[three elemCodes]]
    MAP = 9          # Sends the board game "map"
    DECK = 10        # Cards [[name of enums : strings]]
    TURN_PROMPT = 11 # prompts turn [[key: action string], reason] roll, passage, accuse
    TURN = 20        # response to TURN_PROMPT [actionKey, [promptedKeys]]
    MOVE_PROMPT = 12 # [diceRoll, reason]
    MOVE = 13        # Walk request [charCode, diceSum, moveStr]
    TURN_CONT = 14   # prompts turn [{key: action string}] suggest, accuse
    SUG_PROMPT = 15  # [reason]
    SUGGESTION = 16  # [suggesterId, [keys for things suggested]], sent to server and others
    CARD_SHOW = 17   # [suggesterId, key for card if in hand ] if no cards -> [none, none]
    ACC_PROMPT = 18  # [reason]
    ACCUSE = 19      # [[keys for things accusing]]


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

### Return Types
# Simple strings
basicStrings = {
                Code.EXIT:      'Something went wrong, exiting game.'
               }

# Strings with embedded data
formatStrs = {  Code.START:     'Your id is {0}',
                Code.CHAR_ACC:  '{0} (Player {1}) has selected {3}',
                Code.MAP:       '\n{0}\n',
                Code.DATA:      '\n{0}\n',
             }

# Functions
formatFuncs = {
                Code.CHAR_PROMPT: (lambda d : stringifyList([d[1], "Available characters:"],d[0])),
                Code.DECK: (lambda d : stringifyList(["Your cards:"], *d)),
                Code.TURN_PROMPT: (lambda d : stringifyList(["Turn Options:"], *d)),
              }

def stringifyList(text, list, leftSpace = 35):
    formatStr = '{{0: <{}}} ({{1}})'.format(leftSpace)
    for key in list:
        text.append( formatStr.format(list[key], key))
    return '\n'.join(text)
