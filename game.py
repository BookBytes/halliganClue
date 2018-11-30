#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Reference for declaration
# https://stackoverflow.com/questions/6289474/
# working-with-utf-8-encoding-in-python-source

import random
import itertools
import threading
from game_data import SuspectList, WeaponsList, PlacesList
from game_data import MAP, LOCATIONS, KEY_MAP


def locked(func):
    def wrapper(*args):
        with args[0].lock:
            return func(*args)
    return wrapper

class Deck(object):
    def __init__(self):
        suspects = list(SuspectList)
        weapons = list(WeaponsList)
        places = list(PlacesList)

        char = self.draw(suspects)
        weapon = self.draw(weapons)
        place = self.draw(places)

        self.solution = [char, weapon, place]

        self.userCards = suspects + weapons + places

    def draw(self, deck):
        """ Draws a random card from the given deck.
            Card is removed and returned """
        card = random.choice(deck)
        deck.remove(card)
        return card

    def dealPlayer(self, numPlayers):
        if len(self.userCards) == 0:
            return []  # all cards dealt
        # Reference on range
        # https://stackoverflow.com/questions/3685974/
        # iterate-a-certain-number-of-times-without-storing-the-iteration-number-anywhere
        hand = []
        for _i in range(18/numPlayers):
            card = self.draw(self.userCards)
            hand.append(card)
        return hand

    def checkSolution(self, guess):
        # guess is a tuple structured as follows: (char, weapon, room).
        # Unlike the physical board game the user does not need
        # to see the cards to check so they can guess again.

        #       guess[0] == self.solution[0] and \
        #       guess[1] == self.solution[1] and \
        #       guess[2] == self.solution[2]

        return self.solution == guess


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
    def __init__(self, addrList):

        # FIX ME
        self.lock = threading.Lock()

        self.suspects = list(SuspectList)

        if len(addrList) < 2 or len(addrList) > 6:
            return

        # Characters listed in character player order
        charNames = ['Megan "The Captain" Monroe',
                     'Ming "The Hacker" Chow',
                     'Mark "The Shark" Sheldon',
                     'Megan "The Administrator" Monaghan',
                     'Norman "The Linguist" Ramsey',
                     'Donna "The Coordinator" Cirelli']

        self.characters = {}

        self.mapToSym =  {char: key for key, char in KEY_MAP.iteritems()}

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

        #chars = charNames  # deep copy
        # mapping of ip addresses to character names;
        # use this to index into the "characters," aka character objects
        # NOTE: currently character assignment is random.
        # It works for any number of players between 2 and 6 (check above).
        #self.charMapping = []
        # for addr in addrList:
        #     char = random.choice(chars)
        #     self.charMapping[addr] = char
        #     chars.pop(char)


        self.items = list(WeaponsList)
        places = list(PlacesList)

        # for porting/stepping into a room
        self.rooms = LOCATIONS  # deep copy

        weaponSyms = ["~", "!", "#", "$", "%", "&"]  # to be replaced by images for GUI

        self.weapons = []

        self.deck = Deck()
        self.map = MAP

        for item in self.items:
            room = random.choice(places)
            x, y = LOCATIONS[room]
            weaponSym = random.choice(weaponSyms)
            self.weapons.append(Weapon(x, y, weaponSym))
            self.map = self.map[0:((y*77) + x)] + weaponSym + self.map[((y*77) + x + 1):]  # move this to element class
            places.remove(room)
            weaponSyms.remove(weaponSym)

    def getChar(self, addr):
        # OBS?
        return self.charMapping[addr]

    @locked
    def claimSuspect(self, suspectKey):
        """ Requests a given suspect via suspect code and removes it from list
            if it is still available. Returns character if request is successful,
            false otherwise. Returns reason if failure"""

        if (suspectKey not in KEY_MAP) and not SuspectList.has(KEY_MAP[suspectKey]):
                return (False, "That is not a valid suspect code, try again.")

        suspect = KEY_MAP[suspectKey]

        if suspect in self.suspects:
            self.suspects.remove(suspect)
            return (suspect, None)
        else:
            return (False, "That character is already chosen")

    @locked
    def availableSuspects(self):
        """ Returns a json serializble suspect list """
        return [(self.mapToSym[x], x.value) for x in self.suspects]
