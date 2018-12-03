import json
from enum import Enum
import sys

DATA = "data"

SIZE_DIGITS = 4 # Length of the string representing the message size

def receiveNextMsg(conn):
    """ Receives next set of data based on prepended size information """
    try:
        msgSize = conn.recv(SIZE_DIGITS)
        rawMsg = conn.recv(int(msgSize))
        msg = Message(str = rawMsg)
        return msg
    except:
        print conn.recv(1024)
        return Message(command = Code.EXIT)


class Code(Enum):
    """ Valid message commands """
    NAME = 1         # Sends player name to server
    START = 2        # Send with no data, contacts will append id
    EXIT = 3
    INFO = 4         # This is for misc. data BESIDES map
    CHAR_REQ = 5     # Request a character, [charKey]
    CHAR_PROMPT = 6  # Rejects a character request [available charCodes]
    CHAR_ACC = 7     # Notifies of accepted character request [name, id, charCode, charName]
    MAP = 9          # Sends the board game "map"
    DECK = 10        # Cards [name of enums : strings]
    TURN_PROMPT = 11 # prompts turn [[key: action string]] roll, passage, accuse
    TURN = 20        # response to TURN_PROMPT [actionKey, [promptedKeys]]
    MOVE_PROMPT = 12 # [diceRoll]
    MOVE = 13        # Walk request [diceRoll, moveStr]
    TURN_CONT = 14   # prompts turn [[key: action string]] suggest, accuse
    SUG_PROMPT = 15  # Prompts a suggestion
    SUGGESTION = 16  # [suggesterId, [keys for things suggested]], sent to server and others
    CARD_SHOW = 17   # [suggesterId, key for card if in hand, [cards in hand], [keys for things suggested]] if no cards -> [none, none]
    ACC_PROMPT = 18  # Prompts an accusation
    ACCUSE = 19      # [keys for things accusing]


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
                Code.EXIT:      'Something went wrong, exiting game.',
                Code.ACC_PROMPT: 'Make an accusation',
                Code.SUG_PROMPT: 'Make an suggestion',
                Code.SUGGESTION: 'Show card to disprove this suggestion:'
               }

# Strings with embedded data
formatStrs = {  Code.START:     'Your id is {0}',
                Code.CHAR_ACC:  '{0} (Player {1}) has selected {3}',
                Code.MAP:       '\n{0}\n',
                Code.INFO:      '{0}',
                Code.MOVE_PROMPT: 'Move your character (max {0}):'
             }

# Functions
formatFuncs = {
                Code.CHAR_PROMPT: (lambda d : stringifyDict("Available characters:", d)),
                Code.DECK: (lambda d : stringifyDict("Your cards:", d)),
                Code.TURN_PROMPT: (lambda d : stringifyDict("Action Options:", d)),
                Code.TURN_CONT: (lambda d: stringifyDict("Action Options:", d ))
              }

def stringifyDict(text, dict, leftSpace = 35):
    strArr = [text]
    formatStr = '{{0: <{}}} ({{1}})'.format(leftSpace)
    for key in dict:
        strArr.append( formatStr.format(dict[key], key))
    return '\n'.join(strArr)
