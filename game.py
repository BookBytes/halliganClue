#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Reference for declaration
# https://stackoverflow.com/questions/6289474/
# working-with-utf-8-encoding-in-python-source

import random
import itertools


class Card(object):
    def __init__(self, name, card_img):
        self.name = name
        self.image = card_img


class Deck(object):
    def __init__(self, characters, items, places):
        char = random.choice(characters)
        item = random.choice(items)
        place = random.choice(places)
        self.solution = [char, item, place]
        characters.remove(char)
        items.remove(item)
        places.remove(place)
        first = itertools.chain(characters, items)
        self.userCards = itertools.chain(first, places)

    def dealPlayer(self, numPlayers):
        if len(self.userCards) == 0:
            return []  # all cards dealt
        # Reference on range
        # https://stackoverflow.com/questions/3685974/
        # iterate-a-certain-number-of-times-without-storing-the-iteration-number-anywhere
        hand = []
        for _i in range(18/numPlayers):
            card = random.choice(self.userCards)
            hand.append(card)
            self.userCards.remove(card)
        return hand

    def checkSolution(self, guess):
        # guess is a tuple structured as follows: (char, weapon, room).
        # Unlike the physical board game the user does not need
        # to see the cards to check so they can guess again.
        return guess[0] == self.solution[0] and \
               guess[1] == self.solution[1] and \
               guess[2] == self.solution[2]


class Element(object):
    def __init__(self, x, y, name, img):
        self.location = [x, y]
        self.name = name
        self.image = img

    def getLocation(self):
        return self.location

    def setLocation(self, x, y):  # TODO: take map?
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
    def __init__(self, addrList):
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
        self.characters[charNames[0]] = Suspect(26, 0,   charNames[0], "C")
        self.characters[charNames[1]] = Suspect(46, 0,   charNames[1], "H")
        self.characters[charNames[2]] = Suspect(70, 19,  charNames[2], "S")
        self.characters[charNames[3]] = Suspect(2,  27,  charNames[3], "A")
        self.characters[charNames[4]] = Suspect(70, 27,  charNames[4], "L")
        self.characters[charNames[5]] = Suspect(22, 35,  charNames[5], "c")

        chars = charNames  # deep copy
        # mapping of ip addresses to character names; 
        # use this to index into the "characters," aka character objects
        # NOTE: currently character assignment is random.
        # It works for any number of players between 2 and 6 (check above).
        self.charMapping = []
        for addr in addrList:
            char = random.choice(chars)
            self.charMapping[addr] = char
            chars.pop(char)

        self.items = ['NP = P proof', '105 Textbook',
                      'SQL Injection', 'Binary Bomb', 'Dead squirrel',
                      'Dry white board marker']

        places = ['Collab Room', 'Entryway', 'EECS Office',
                  'Kitchen', 'Fishbowl', 'The Computer Lab',
                  'Couches', 'Admin Office', 'Extension']

        # for porting/stepping into a room
        roomLocations = {places[0]: (4, 9), places[1]: (4, 35), places[2]: (5, 63),
                         places[3]: (18, 9), places[4]: (14, 63), places[5]: (22, 63),
                         places[6]: (31, 9), places[7]: (32, 37), places[8]: (32, 63)}

        self.rooms = roomLocations  # deep copy

        weaponSyms = ["~", "!", "#", "$", "%", "&"]  # to be replaced by images for GUI

        self.weapons = []

        self.deck = Deck(charNames[:], self.items[:], places[:])  # Ensure copy is passed
        self.map = "+=======================================================================+\n" \
                   "|                   |   | C |               | H |   |   |               |\n" \
                   "|                   ---------               -------------               |\n" \
                   "|    Collab Room    |   |                       |   |   |               |\n" \
                   "|                   -----                       ---------  EECS Office  |\n" \
                   "|                   |   >       Entryway        <   |   |               |\n" \
                   "|------------ ^ ---------                       -------------           |\n" \
                   "|   |   |   |   |   |   |                       |   |   |   >           |\n" \
                   "|---------------------------- ^ --------- ^ ----------------------------|\n" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n" \
                   "|-----------------------------------------------------------------------|\n" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   >               |\n" \
                   "|--------------------------------------------------------               |\n" \
                   "|                   |   |   |                   |   |   |   Fishbowl    |\n" \
                   "|                   ---------    ___      ___   ---------               |\n" \
                   "|                   <   |   |    | |      | |   |   |   |               |\n" \
                   "|                   ---------    | |______| |   ----------------- ^ ----|\n" \
                   "|      Kitchen      |   |   |    |  ______  |   |   |   |   |   |   |   |\n" \
                   "|                   ---------    | |      | |   ------------------------|\n" \
                   "|                   |   |   |    |_|      |_|   |   |   |   |   |   | S |\n" \
                   "|                   ---------                   ------------- v --------|\n" \
                   "|                   |   |   |                   |   |   |               |\n" \
                   "|------------ ^ -----------------------------------------               |\n" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   >   Computer    |\n" \
                   "|--------------------------------------------------------      Lab      |\n" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   |               |\n" \
                   "|------------------------------------ v --------------------------------|\n" \
                   "| A |   |   |   |   |   |   |                   |   |   |   |   |   | L |\n" \
                   "|---------------- v ---------                   ------------------------|\n" \
                   "|                   |   |   |                   <   |   |   |   |   |   |\n" \
                   "|                   ---------       Admin       --------- v ------------|\n" \
                   "|                   |   |   |       Office      |   |   |               |\n" \
                   "|      Couches      ---------                   ---------               |\n" \
                   "|                   |   |   |                   |   |   |   Extension   |\n" \
                   "|                   ---------                   ---------               |\n" \
                   "|                   | c |   |                   |   |   |               |\n" \
                   "+=======================================================================+"

        for item in self.items:
            room = random.choice(places)
            x, y = roomLocations[room]
            weaponSym = random.choice(weaponSyms)
            self.weapons.append(Weapon(x, y, item, weaponSym))
            self.map = self.map[0:((y*77) + x)] + weaponSym + self.map[((y*77) + x + 1):]  # move this to element class
            places.remove(room)
            weaponSyms.remove(weaponSym)

    def getChar(self, addr):
        return self.charMapping[addr]
