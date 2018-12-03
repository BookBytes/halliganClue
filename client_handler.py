
from game_data import Actions
from message import Message, Code, receiveNextMsg
from game import Game
import sys

class ClientHandler:
    def __init__(self, id, game, contacts):
        self.id = id
        self.game = game
        self.contacts = contacts

        self.actionHandlers = { Actions.ROLL    : self.roll,
                                Actions.SNEAK   : self.sneak,
                                Actions.ACCUSE  : self.startAccuse }

        self.handleMsgCode = {  Code.NAME:      self.setName,
                                Code.CHAR_REQ:  self.charRequest,
                                Code.EXIT:      self.leave,
                                Code.TURN:      self.turn,
                                Code.MOVE:      self.move,
                                Code.ACCUSE:    self.accuse }

    @classmethod
    def start(self, idSelf, game, contacts):
        """ Called as target by server when starting threads.
            Creates and runs a new ClientHandler instance. """
        handler = self(idSelf, game, contacts)
        handler.loop()

    def loop(self):
        self.gameInProgress = True
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
        self.contacts.notifyAll(Code.INFO, ["{} has RVSPed".format(self.name)])

    def leave(self, _game , _data):
        self.contacts.notifyAll(Code.EXIT)
        self.gameInProgress = False

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
            if cont == True:  # All guests have RSVPed
                self.contacts.notifyAll(Code.INFO,
                                        ["Once you arrive you discover to your "
                                        + "horror that your host, Dr. Fisher, "
                                        + "has been murdered. Did the hacker "
                                        + "hijack her life? Did the captain "
                                        + "guide her to rocky shores? Who "
                                        + "administrated her final night? "
                                        + "The butler whispers to you, hands "
                                        + 'shaking, "It is up to you to find '
                                        + 'out the truth. Please solve this '
                                        + 'terrible crime."'])
                self.contacts.notifyAll(Code.MAP, [self.game.map])
                self.nextTurn(self.contacts.first, game)
        else:
            self.contacts.notify(   self.id,
                                    Code.CHAR_PROMPT,
                                    [ game.availableSuspects(),
                                     cont ])

    def turn(self, game, data):
        actKey, actionOpts = data
        action, feedback = game.canTakeAction(self.character, actKey, actionOpts)
        if feedback:
            self.contacts.notify(   self.id,
                                    Code.TURN_PROMPT,
                                    [ game.startTurnActions(), feedback])
        else:
            self.actionHandlers[action](game)

    def move(self, game, data):
        diceRoll, movement = data
        success, feedback = game.move(self.character, diceRoll, movement)
        if success:
            self.contacts.notifyAll(Code.MAP, [self.game.map])
            moveStr = "{} moved to {}".format(self.character.value, feedback)
            self.contacts.notifyAll(Code.INFO, [moveStr])
            contActions = self.game.continueTurnActions(self.character)
            self.contacts.notify(   self.id,
                                    Code.TURN_CONT,
                                    [ contActions,
                                      "Would you like to take further action?"])
        else:
            self.contacts.notify(   self.id,
                                    Code.MOVE_PROMPT,
                                    [ diceRoll, feedback] )
    def accuse(self, game, data):
        murderer, weapon, location = data
        print murderer
        print weapon
        print location
        success, feedback = game.checkSolution( weaponK = weapon,
                                                murdererK = murderer,
                                                placeK = location)
        if success == -1:
            # Invalid
            self.contacts.notify(self.id, Code.ACC_PROMPT, [feedback])
        elif success == 0:
            # Incorrect
            self.contacts.notifyAll( Code.INFO, ["Accusation incorrect"])
            next = self.contacts.nextId(self.id)
            # Remove from turn order
            self.nextTurn(next, game)
        else:
            #Correct
            self.contacts.notifyAll( Code.INFO, ["Congratulations " +
                                                 self.id +
                                                 "guessed correctly. \
                                                 The tragic murder is solved!"])


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
        self.contacts.notifyAll( Code.INFO,
                                 ["{} rolled {}".format(self.name, dice)])
        self.contacts.notify(   self.id,
                                Code.MOVE_PROMPT,
                                [dice, ""] )

##############################################################################

    def nextTurn(self, id, game):
        self.contacts.notify(   id,
                                Code.TURN_PROMPT,
                                [ game.startTurnActions(), ""])
