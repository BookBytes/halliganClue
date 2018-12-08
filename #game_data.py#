from enum import Enum

class SuspectList(Enum):
    MEGAN_C = 'Megan "The Captain" Monroe'
    MING = 'Ming "The Hacker" Chow'
    MARK = 'Mark "The Shark" Sheldon'
    MEGAN_A = 'Megan "The Administrator" Monaghan'
    NORMAN = 'Norman "The Linguist" Ramsey'
    DONNA = 'Donna "The Coordinator" Cirelli'

class WeaponsList(Enum):
    MARKER = 'Dry white board marker'
    BOOK = '105 Textbook'
    BOMB = 'Binary Bomb'
    SQUIRREL = 'Dead squirrel'
    SQL = 'SQL Injection'
    PROOF = 'NP = P proof'

class PlacesList(Enum):
    COLLAB = 'Collab Room'
    ENTRY = 'Entryway'
    EECS = 'EECS Office'
    KITCHEN = 'Kitchen'
    BOWL = 'Fishbowl'
    LAB = 'The Computer Lab'
    COUCHES = 'Couches'
    ADMIN = 'Admin Office'
    EXTEN = 'Extension'

class Actions(Enum):
    ROLL = "Roll the dice to move"
    SNEAK = "Take a secret passage way"
    ACCUSE = "Make an accusation"
    SUGGEST = "Make a suggestion"
    FINISH = "Finish your turn"


LOCATIONS = {PlacesList.COLLAB: {(2,3)}, PlacesList.ENTRY: {(2,6),(2,11),\
             (3,7),(3,10)}, PlacesList.EECS: {(3,15)},
             PlacesList.KITCHEN: {(7,5),(10,4)}, PlacesList.BOWL: {(5,14),(7,16)}, PlacesList.LAB: {(10,15),(11,14)},
             PlacesList.COUCHES: {(14,4)}, PlacesList.ADMIN: {(13,9),(14,11)}, PlacesList.EXTEN: {(15,14)}}



# Reversed in mapToSym in game
KEY_MAP = { "C" : SuspectList.MEGAN_C,
            "H" : SuspectList.MING,
            "S" : SuspectList.MARK,
            "A" : SuspectList.MEGAN_A,
            "L" : SuspectList.NORMAN,
            "c" : SuspectList.DONNA,

            "1" : PlacesList.COLLAB,
            "2" : PlacesList.ENTRY,
            "3" : PlacesList.EECS,
            "4" : PlacesList.KITCHEN,
            "5" : PlacesList.BOWL,
            "6" : PlacesList.LAB,
            "7" : PlacesList.COUCHES,
            "8" : PlacesList.ADMIN,
            "9" : PlacesList.EXTEN,

            "!" : WeaponsList.MARKER,
            "@" : WeaponsList.BOMB,
            "#" : WeaponsList.BOOK,
            "$" : WeaponsList.SQUIRREL,
            "%" : WeaponsList.SQL,
            "^" : WeaponsList.PROOF,

            "r" : Actions.ROLL,
            "p" : Actions.SNEAK,
            "a" : Actions.ACCUSE,
            "s" : Actions.SUGGEST,
            "d" : Actions.FINISH

            }


MAP =  "+=======================================================================+\n" \
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

location = {(x,y) for x in range(18) for y in range(18)}
location.difference_update({(x,y) for x in range(3) for y in range(5)})
location.difference_update({(0,y) for y in range(7,11,1)})
location.difference_update({(x,y) for y in range(6,12,1) for x in range(1,4,1)})
location.difference_update({(x,y) for x in range(3) for y in range(14,18,1)})
location.difference_update({(3,y) for y in range(15,18,1)})

location.difference_update({(x,y) for x in range(6,11,1) for y in range(5)})
location.difference_update({(x,y) for x in range(6,11,1) for y in range(7,12,1)})
location.difference_update({(x,y) for x in range(5,8,1) for y in range(14,18,1)})
location.difference_update({(x,y) for x in range(10,13,1) for y in range(14,18,1)})
location.difference_update({(x,y) for x in range(14,18,1) for y in range(5)})
location.difference_update({(x,y) for x in range(13,18,1) for y in range(7,12,1)})
location.difference_update({(x,y) for x in range(15,18,1) for y in range(14,18,1)})

location.add((2,3))
location.add((2,6))
location.add((2,11))
location.add((3,7))
location.add((3,10))
location.add((3,15))
location.add((5,14))
location.add((7,4))
location.add((7,16))
location.add((10,3))
location.add((10,15))
location.add((11,14))
location.add((13,9))
location.add((14,4))
location.add((14,11))
location.add((15,14)) 
