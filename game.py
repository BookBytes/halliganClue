#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Reference for declaration
# https://stackoverflow.com/questions/6289474/
# working-with-utf-8-encoding-in-python-source

import random
import itertools
import threading
from game_data import SuspectList, WeaponsList, PlacesList, Actions
from game_data import MAP, LOCATIONS, KEY_MAP


def locked(func):
    def wrapper(*args):
        with args[0].lock:
            return func(*args)
    return wrapper

class Deck(object):
    def __init__(self, numPlayers):
        suspects = list(SuspectList)
        weapons = list(WeaponsList)
        places = list(PlacesList)

        self.murderer = self.draw(suspects)
        self.weapon = self.draw(weapons)
        self.place = self.draw(places)

        self.userCards = suspects + weapons + places
        self.handSize = len(self.userCards)/numPlayers

    def draw(self, deck):
        """ Draws a random card from the given deck.
            Card is removed and returned """
        card = random.choice(deck)
        deck.remove(card)
        return card

    def dealPlayer(self):
        if len(self.userCards) == 0:
            return []  # all cards dealt
        # Reference on range
        # https://stackoverflow.com/questions/3685974/
        # iterate-a-certain-number-of-times-without-storing-the-iteration-number-anywhere
        hand = []
        for _i in range(self.handSize):
            card = self.draw(self.userCards)
            hand.append(card)
        return hand

    def checkSolution(self, weapon = None,
                            murderer = None,
                            place = None):
        return self.weapon == weapon and\
               self.murderer == murderer and\
               self.place == place


class Element(object):
    def __init__(self, x, y, symbol):
        self.location = [x, y]
        self.sym = symbol

    def getLocation(self):
        return self.location

    def setLocation(self, x, y):  # TODO: take map?
        self.location = [x, y]


class Suspect(object):
    def __init__(self, x, y, sym):
        self.element = Element(x, y, sym)

    def walk(self, directions):
        currX, currY = self.element.getLocation()
        xMovement = 0
        yMovement = 0

        for direction in directions:
            if direction == "^":
                xMovement -= 1
            elif direction == "<":
                yMovement -= 1
            elif direction == ">":
                yMovement += 1
            elif direction == "v":
                xMovement += 1
            else:
                return "Invalid direction " + direction + " provided"

        self.element.setLocation(currX + xMovement, currY + yMovement)

class Weapon(object):
    def __init__(self, x, y, sym):
        self.element = Element(x, y, sym)


class Game(object):
    def __init__(self, numPlayers):

        # FIX ME
        self.lock = threading.Lock()
        self.suspects = list(SuspectList)
        self.numPlayers = numPlayers

        if self.numPlayers < 2 or self.numPlayers > 6:
            return


        self.mapToSym =  {char: key for key, char in KEY_MAP.iteritems()}

        self.characters= {}

        self.characters[SuspectList.MEGAN_C] = Suspect(26, 0,
                                            self.mapToSym[SuspectList.MEGAN_C])
        self.characters[SuspectList.MING] = Suspect(46, 0,
                                            self.mapToSym[SuspectList.MING])
        self.characters[SuspectList.MARK] = Suspect(70, 19,
                                            self.mapToSym[SuspectList.MARK])
        self.characters[SuspectList.MEGAN_A] = Suspect(2,  27,
                                            self.mapToSym[SuspectList.MEGAN_A])
        self.characters[SuspectList.NORMAN] = Suspect(70, 27,
                                            self.mapToSym[SuspectList.NORMAN])
        self.characters[SuspectList.DONNA] = Suspect(22, 35,
                                            self.mapToSym[SuspectList.DONNA])


        self.items = list(WeaponsList)
        places = list(PlacesList)

        # for porting/stepping into a room
        self.rooms = LOCATIONS  # deep copy

        weaponSyms = ["~", "!", "#", "$", "%", "&"]
        self.weapons = []

        self.deck = Deck(numPlayers)
        self.map = MAP

        for item in self.items:
            room = random.choice(places)
            rdata = LOCATIONS[room]
            print rdata
            x, y = rdata
            weaponSym = random.choice(weaponSyms)
            self.weapons.append(Weapon(x, y, weaponSym))
            self.map = self.map[0:((y*77) + x)] + weaponSym + self.map[((y*77) + x + 1):]
            places.remove(room)
            weaponSyms.remove(weaponSym)


    @locked
    def claimSuspect(self, suspectKey):
        """ Tries to claim specified character.
            Args:
                Suspect key
            Returns:
                success  -  character if successful,
                            False otherwise
                feedback -  if claim is successful:
                                True if all players have claimed suspects
                                False otherwise
                            error message if claim fails,
        """

        if (suspectKey not in KEY_MAP) or\
            not isinstance(KEY_MAP[suspectKey], SuspectList):
                return (False, "That is not a valid suspect code, try again.")

        suspect = KEY_MAP[suspectKey]

        if suspect in self.suspects:
            self.suspects.remove(suspect)
            return (suspect, len(self.suspects) == 6 - self.numPlayers)
        else:
            return (False, "That character is already chosen")


    def toKeyDict(self, list):
        """ Converts list to key: string dictionary"""
        return {self.mapToSym[x]:x.value for x in list}

    @locked
    def availableSuspects(self):
        """ Returns a dict suspect list """
        return self.toKeyDict(self.suspects)

    @locked
    def getHand(self):
        """ Returns dictionary of cards. """
        cards = self.deck.dealPlayer()
        return self.toKeyDict(cards)

    def startTurnActions(self):
        """ Returns dictionary of actions performable
            at start of turn. """
        actions = [Actions.ROLL, Actions.SNEAK, Actions.ACCUSE]
        return self.toKeyDict(actions)

    def continueTurnActions(self, character):
        """ Returns dictionary of actions a character can
            perform given their location. """
        # If character is in room, allow suggestions
        actions = [Actions.ACCUSE, Actions.SUGGEST, Actions.FINISH]
        return self.toKeyDict(actions)

    def canTakeAction(self, character, actionKey, actionOpts):
        """ Moves the character to a new board location.
            Args:
                Character Enumeration
                Action key
                List of offered action keys
            Returns:
                success  -  Action enum if allowed
                            False if action not allowed,
                feedback -  None if successful
                            error message if failure,
                            """
        failure = None
        if actionKey not in actionOpts:
            return (False, "That is not an available action. Try again:")

        characterCant = False # TODO: FIX ME
        if characterCant:
            return (False,
                    "You cannot take this action at this time. Try again:")

        return (KEY_MAP[actionKey], None)

    @locked
    def move(self, character, roll, movement):
        """ Moves the character to a new board location.
            Args:
                Character key
                Dice roll number
                Movement String
            Returns:
                success  - boolean, was move successful
                feedback - new location if successful
                           error message if failure"""

        return (True, "Kitchen")

    def roll(self):
        return random.randint(1, 6)

    def isValidTrio(self,   weaponK = None,
                            murdererK = None,
                            placeK = None):
        """ Checks game solution.
            Args:
                guess - keys for [murderer, weapon, place]
            Returns:
                success  -  {murderer, weapon, place} if valid,
                            False otherwise
                feedback -  None if successful
                            First failure reason if not valid """
        trio = {"murderer": None, "weapon": None, "place": None}
        if murdererK in KEY_MAP and \
                isinstance(KEY_MAP[murdererK], SuspectList):
            trio["murderer"] = KEY_MAP[murdererK]
        else:
            return (False, "That is not a suspect, please try again")
        if weaponK in KEY_MAP and \
            isinstance(KEY_MAP[weaponK], WeaponsList):
            trio["weapon"] = KEY_MAP[weaponK]
        else:
            return (False, "That is not a weapon, please try again")
        if placeK in KEY_MAP and \
            isinstance(KEY_MAP[placeK], PlacesList):
            trio["place"]= KEY_MAP[placeK]
        else:
            return (False, "That is not a place, please try again")
        return (trio, "")

    def checkSolution(self, weaponK = None,
                            murdererK = None,
                            placeK = None):
        """ Checks game solution.
            Args:
                guess - keys for [murderer, weapon, place]
            Returns:
                success  -  -1 if not valid
                             1 if valid and successful,
                             0 otherwise
                feedback -  Proposed solution if valid
                            Failure reason if not valid """

        success, feedback = self.isValidTrio(weaponK, murdererK, placeK)
        if success:
            correct = self.deck.checkSolution( weapon = success["weapon"],
                                               murderer = success["murderer"],
                                               place = success["place"] )
            if correct:
                return (1, success)
            else:
                return (0, success)
        else:
            return (-1, feedback)
