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
                                Actions.ACCUSE  : self.startAccuse,
                                Actions.SUGGEST : self.startSuggestion,
                                Actions.FINISH  : self.finishTurn }

        self.handleMsgCode = {  Code.NAME:      self.setName,
                                Code.CHAR_REQ:  self.charRequest,
                                Code.EXIT:      self.leave,
                                Code.TURN:      self.turn,
                                Code.MOVE:      self.move,
                                Code.ACCUSE:    self.accuse,
                                Code.SUGGESTION:self.suggest,
                                Code.CARD_SHOW: self.showCards }

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
                self.handleMsgCode[msg.command](msg.data)

##############################################################################
### Code for handling each message code
### Arguments
###		self
###     self.game
###		data - data from message packet
##############################################################################
    def setName(self, data):
        [self.name] = data
        self.contacts.notifyAll(Code.INFO, ["{} has RVSPed".format(self.name)])

    def leave(self, _data):
        self.contacts.notifyAll(Code.EXIT)
        self.gameInProgress = False

    def charRequest(self, data):
        [charKey] = data
        char, feedback = self.game.claimSuspect(charKey)
        if char:
            self.character = char
            self.contacts.notifyAll(Code.CHAR_ACC,
                                [self.name, self.id, char.name, char.value])
            self.deck = self.game.getHand()
            self.contacts.notify( self.id, Code.DECK, self.deck )
            if feedback == True:
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
                self.nextTurn(self.contacts.first)
        else: # Character already taken
            self.informSelf(feedback)
            self.contacts.notify(   self.id,
                                    Code.CHAR_PROMPT,
                                    self.game.availableSuspects() )

    def turn(self, data):
        actKey, actionOpts = data
        action, feedback = self.game.canTakeAction(self.character,
                                                        actKey, actionOpts)
        if feedback:
            self.informSelf(feedback)
            self.nextTurn( self.id )
        else:
            self.actionHandlers[action]()

    def move(self, data):
        diceRoll, movement = data
        success, feedback = self.game.move(self.character, diceRoll, movement)
        if success:
            self.contacts.notifyAll(Code.MAP, [self.game.map])
            moveStr = "{} moved to {}".format(self.character.value, feedback)
            self.contacts.notifyAll(Code.INFO, [moveStr])
            contActions = self.game.continueTurnActions(self.character)
            self.contacts.notify(   self.id,
                                    Code.TURN_CONT,
                                    contActions )
        else:
            self.informSelf(feedback)
            self.contacts.notify(   self.id,
                                    Code.MOVE_PROMPT,
                                    [ diceRoll ] )
    def accuse(self, data):
        murderer, weapon, location = data
        success, feedback = self.game.checkSolution( weaponK = weapon,
                                                     murdererK = murderer,
                                                     placeK = location)
        if success == -1:
            # Invalid
            self.informSelf(feedback)
            self.contacts.notify( self.id, Code.ACC_PROMPT )
        elif success == 0:
            # Incorrect
            self.contacts.notifyAll( Code.INFO, ["Evidence comes to light"
                                                 + " proving Player "
                                                 + str(self.id)
                                                 + "'s accusation"
                                                 + " to be incorrect. They"
                                                 + " get the sense that if"
                                                 + " they were to accuse"
                                                 + " anyone else the others"
                                                 + " would not believe them."
                                                 + " Player" + str(self.id)
                                                 + " decides to follow"
                                                 + " the others around and"
                                                 + " see what they find"
                                                 + " instead."])
            next = self.contacts.nextId(self.id)
            self.contacts.remove(self.id)
            self.nextTurn(next)
        else:
            #Correct
            self.contacts.notifyAll( Code.INFO, ["Congratulations " +
                                                 self.id +
                                                 " guessed correctly." +
                                                 " The tragic murder is solved."])

    def suggest(self, data):
        suggesterId, [murderer, weapon, location] = data
        success, feedback = self.game.isValidTrio(  murdererK = murderer,
                                                    weaponK = weapon,
                                                    placeK = location )
        if success:
            suggestStr = '{} has made a suggestion: \n{} in the {} with the {}'

            self.contacts.notifyAll( Code.INFO,
                                     [suggestStr.format( self.name,
                                                success["murderer"].value,
                                                success["place"].value,
                                                success["weapon"].value )])
            next = self.contacts.nextId(self.id)
            self.contacts.notify( next, Code.SUGGESTION, data )
        else:
            self.informSelf(feedback)
            self.contacts.notify( self.id, Code.SUG_PROMPT )

    def showCards(self, data):
        id, key, keyDict, sugKeys = data
        if keyDict: # Player had a match
            if key in keyDict: # Valid key provided
                self.contacts.notifyAll(Code.INFO,
                                ["{} showed a card.".format(self.name)])
                notifyStr = "{} showed you {}".format(self.name,
                                                keyDict[key])
                self.contacts.notify(id, Code.INFO, [notifyStr])
                self.nextTurn(self.contacts.nextId(id))
            else: # invalid key
                self.contacts.notify(   self.id,
                                        Code.INFO,
                                        ["That is not one of your cards."])
                self.contacts.notify(   self.id,
                                        Code.SUGGESTION,
                                        [id, sugKeys])
        else: # Player had no match
            next = self.contacts.nextId(self.id)
            if next == id: # Gone full circle
                self.contacts.notifyAll( self.INFO,
                                        ["No one had a card."])
                # Turn goes to player after suggestor
                self.nextTurn( self.contacts.nextId(next) )
            else: #Pass suggestion on
                self.contacts.notifyAll(Code.INFO,
                            ["{} did not show a card.".format(self.name)])
                self.contacts.notify(   next,
                                        Code.SUGGESTION,
                                        [id, sugKeys])

    #def evalSuggestion(self, data):



##############################################################################
### Action Handlers
### Arguments
###		self
###     self.game
##############################################################################
    def startAccuse(self):
        self.contacts.notify( self.id, Code.ACC_PROMPT)

    def sneak(self):
        # Actually should do something
        self.finishTurn()

    def roll(self):
        dice = self.game.roll()
        self.contacts.notifyAll( Code.INFO,
                                 ["{} rolled {}".format(self.name, dice)])
        self.contacts.notify( self.id, Code.MOVE_PROMPT, [dice])

    def startSuggestion(self):
        self.contacts.notify( self.id, Code.SUG_PROMPT)

    def finishTurn(self):
        self.nextTurn(self.contacts.nextId(self.id))

##############################################################################
##      Common actions
##############################################################################

    def nextTurn(self, id):
        self.contacts.notify(   id,
                                Code.TURN_PROMPT,
                                self.game.startTurnActions() )

    def informSelf(self, text):
        self.contacts.notify(   self.id,
                                Code.INFO,
                                [text])
