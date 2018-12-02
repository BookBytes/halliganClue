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
    MOVE = 1
    SUGGEST = 2
    ACCUSE = 2

LOCATIONS = {PlacesList.COLLAB: (4, 9), PlacesList.ENTRY: (4, 35), PlacesList.EECS: (5, 63),
             PlacesList.KITCHEN: (18, 9), PlacesList.BOWL: (14, 63), PlacesList.LAB: (22, 63),
             PlacesList.COUCHES: (31, 9), PlacesList.ADMIN: (32, 37), PlacesList.EXTEN: (32, 63)}



# The inverse key_map exists as mapToSym in the game object
KEY_MAP = { "C" : SuspectList.MEGAN_C,
            "H" : SuspectList.MING,
            "S" : SuspectList.MARK,
            "A" : SuspectList.MEGAN_A,
            "L" : SuspectList.NORMAN,
            "c" : SuspectList.DONNA }


MAP = "+=======================================================================+\n" \
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
