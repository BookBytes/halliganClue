
from game_data import Actions
from message import Message, Code, receiveNextMsg
from game import Game

class ClientHandler:
    def __init__(self, id, game, contacts):
        self.id = id
        self.game = game
        self.contacts = contacts

        self.gameInProgress = True

        self.actionHandlers = { Actions.ROLL    : self.roll,
                                Actions.SNEAK   : self.sneak,
                                Actions.ACCUSE  : self.startAccuse }

        self.handleMsgCode = {  Code.NAME:      self.setName,
                                Code.CHAR_REQ:  self.charRequest,
                                Code.EXIT:      self.leave,
                                Code.TURN:      self.turn }

    @classmethod
    def start(self, idSelf, game, contacts):
        """ Called as target by server when starting threads.
            Creates and runs a new ClientHandler instance. """
        handler = self(idSelf, game, contacts)
        handler.loop()

    def loop(self):
        connSelf = self.contacts[ self.id ]
        while self.gameInProgress:
            msg = receiveNextMsg( connSelf )
            print "received data:", msg.command, msg.data
            if msg.command in self.handleMsgCode:
                self.handleMsgCode[msg.command](self.game, msg.data)

##############################################################################
### Code for handling each message code
### Arguments
###		self
###     game
###		data - data from message packet
##############################################################################
    def setName(self, _game, data):
        [self.name] = data
        self.contacts.notifyAll(Code.DATA, ["{} has joined the game".format(self.name)])

    def leave(self, _game , _data):
        self.contacts.notifyAll(Code.EXIT)
        exit()

    def charRequest(self, game, data):
        [charKey] = data
        char, cont = game.claimSuspect(charKey)
        if char:
            self.character = char
            self.contacts.notifyAll(Code.CHAR_ACC,
                                    [self.name, self.id, char.name, char.value])
            self.deck = game.getHand()
            self.contacts.notify(   self.id,
                                    Code.DECK,
                                    [ self.deck ])
            if cont == True:
                self.contacts.notifyAll(Code.DATA,
                                        "All players have selected characters. Ready to begin.")
                self.contacts.notifyAll(Code.MAP, [self.game.map])
                self.contacts.notify(   self.contacts.first,
                                        Code.TURN_PROMPT,
                                        [ game.startTurnActions(), ""])
        else:
            self.contacts.notify(   self.id,
                                    Code.CHAR_PROMPT,
                                    [ game.availableSuspects(),
                                     cont ])

    def turn(self, game, data):
        actKey, actionOpts = data
        action, err = game.canTakeAction(self.character, actKey, actionOpts)
        if err:
            self.contacts.notify(   self.id,
                                    Code.TURN_PROMPT,
                                    [ game.startTurnActions(), err ])
        else:
            self.actionHandlers[action](game)

##############################################################################
### Action Handlers
### Arguments
###		self
###     game
##############################################################################
    def startAccuse(self, game):
        self.contacts.notify(   self.id,
                                Code.ACC_PROMPT,
                                [""] )

    def sneak(self, game):
        pass

    def roll(self, game):
        dice = game.roll()
        self.contacts.notifyAll( Code.DATA,
                                 ["{} rolled {}".format(self.name, dice)])
        self.contacts.notify(   self.id,
                                Code.MOVE_PROMPT,
                                [dice, ""] )

##############################################################################
