import random
import itertools


class Card(object):
    def __init__(self, name, card_img):
        self.name = name
        self.image = card_img


class Deck(object):
    def __init__(self):
        characters = ['Donna “The Coordinator” Cirelli',
                      'Mark "The Shark" Sheldon',
                      'Megan “The Administrator” Monaghan ',
                      'Megan "The Captain" Monroe ',
                      'Ming “The Hacker” Chow',
                      'Norman “The Linguist” Ramsey']
        items = ['NP = P proof', '105 Textbook',
                 'SQL Injection', 'Binary Bomb', 'Dead squirrel',
                 'Dry white board marker']
        places = ['Collab Room', 'Entry way', 'EECS Office',
                  'Kitchen', 'Fishbowl', 'The Computer Lab', 'Couches',
                  'Admin Office', 'Extension']
        char = random.choice(characters)
        item = random.choice(items)
        place = random.choice(places)
        self.solution = [char, item, place]
        characters.remove(char)
        items.remove(item)
        places.remove(place)
        first = itertools.chain(characters, items)
        self.userCards = itertools.chain(first, places)

    def deal(self):
        return

    def checkSolution(self):
        return


class Element(object):
    def __init__(self, x, y, name, img):
        self.location = [x, y]
        self.name = name
        self.image = img

    def relocateTo(self):
        return


class Suspect(object):
    def __init__(self, x, y, name, img):
        self.element = Element(x, y, name, img)

    def startingLocation(self):
        return

    def walk(self):
        return


class Weapon(object):
    def __init__(self, x, y, name, img):
        self.element = Element(x, y, name, img)


class Game(object):
    def __init__(self):
        self.deck = Deck()
        self.map = "+=======================================================================+" \
                   "|                   |   |   |               |   |   |   |               |" \
                   "|                   ---------               -------------               |" \
                   "|    Collab Room    |   |                       |   |   |               |" \
                   "|                   -----                       ---------  EECS Office  |" \
                   "|                   |   >       Entryway        <   |   |               |" \
                   "|------------ ^ ---------                       -------------           |" \
                   "|   |   |   |   |   |   |                       |   |   |   >           |" \
                   "|---------------------------- ^ --------- ^ ----------------------------|" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |" \
                   "|-----------------------------------------------------------------------|" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   >               |" \
                   "|--------------------------------------------------------               |" \
                   "|                   |   |   |                   |   |   |   Fishbowl    |" \
                   "|                   ---------    ___      ___   ---------               |" \
                   "|                   <   |   |    | |      | |   |   |   |               |" \
                   "|                   ---------    | |______| |   ----------------- ^ ----|" \
                   "|      Kitchen      |   |   |    |  ______  |   |   |   |   |   |   |   |" \
                   "|                   ---------    | |      | |   ------------------------|" \
                   "|                   |   |   |    |_|      |_|   |   |   |   |   |   |   |" \
                   "|                   ---------                   ------------- v --------|" \
                   "|                   |   |   |                   |   |   |               |" \
                   "|------------ ^ -----------------------------------------               |" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   >   Computer    |" \
                   "|--------------------------------------------------------      Lab      |" \
                   "|   |   |   |   |   |   |   |   |   |   |   |   |   |   |               |" \
                   "|------------------------------------ v --------------------------------|" \
                   "|   |   |   |   |   |   |   |                   |   |   |   |   |   |   |" \
                   "|---------------- v ---------                   ------------------------|" \
                   "|                   |   |   |                   <   |   |   |   |   |   |" \
                   "|                   ---------       Admin       --------- v ------------|" \
                   "|                   |   |   |       Office      |   |   |               |" \
                   "|      Couches      ---------                   ---------               |" \
                   "|                   |   |   |                   |   |   |   Extension   |" \
                   "|                   ---------                   ---------               |" \
                   "|                   |   |   |                   |   |   |               |" \
                   "+=======================================================================+"
