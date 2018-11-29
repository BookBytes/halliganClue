#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Reference for declaration
# https://stackoverflow.com/questions/6289474/
# working-with-utf-8-encoding-in-python-source

import random
import itertools
import threading
from game_data import SuspectList, WeaponsList, PlacesList, MAP, LOCATIONS


class Card(object):
    def __init__(self, name, card_img):
        self.name = name
        self.image = card_img

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
            return [] # all cards dealt
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
    def __init__(self, x, y, name, img):
        self.location = [x, y]
        self.name = name
        self.image = img

    def getLocation(self):
        return self.location

    def setLocation(self, x, y): # take map?
        self.location = [x, y]


class Suspect(object):
    def __init__(self, x, y, name, img):
        self.element = Element(x, y, name, img)

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
    def __init__(self, x, y, name, img):
        self.element = Element(x, y, name, img)


class Game(object):
    def __init__(self):
        self.lock = threading.Lock()

        self.suspects = list(SuspectList)

        items = list(WeaponsList)
        places = list(PlacesList)

        # for porting/stepping into a room
        self.rooms = LOCATIONS  # deep copy

        weaponSyms = ["~", "!", "#", "$", "%", "&"]  # to be replaced by images for GUI

        self.weapons = []

        self.deck = Deck()
        self.map = MAP

        for item in items:
            room = random.choice(places)
            x, y = LOCATIONS[room]
            weaponSym = random.choice(weaponSyms)
            self.weapons.append(Weapon(x, y, item, weaponSym))
            self.map = self.map[0:((y*77) + x)] + weaponSym + self.map[((y*77) + x + 1):]  # move this to element class
            places.remove(room)
            weaponSyms.remove(weaponSym)

    def claim_suspect(self, suspect_code):
        """ Requests a given suspect via suspect code and removes it from list
            if it is still available. Returns true if request is successful,
            false otherwise. """
        if not SuspectList.has(suspect_code):
            return (False, "That is not a valid suspect code, check your spelling.")

        suspect = SuspectList[suspect_code]
        with self.lock:
            if suspect in self.suspects:
                self.suspects.remove(suspect)
                return (True, None)
            else:
                return (False, "That character is already chosen")

    def available_suspects(self):
        """ Returns a json serializble suspect list """
        with self.lock:
            return [repr(x) for x in self.suspects]
