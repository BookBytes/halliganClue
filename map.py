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




#Location is the representation of position of each character
character = {
'C' : (0,6),
'H' : (0,11),
'S' : (9,17),
'A' : (13,0),
'L' : (13,17),
'c' : (17,5)
}

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

def get_map(x, y):
       return MAP[x*74+y]

def moves (charac, commands):
       global MAP
       x,y = character[charac]
       for command in commands:
              a = move(charac, command)
              if a == 0:
                     new_x, new_y = character[charac]
                     loc2 = 74*(2*new_x+1) + 4*new_y + 1
                     MAP = MAP[:(loc2+1)] + " " + MAP[loc2+2:]
                     loc1 = 74*(2*x+1) + 4*y + 1
                     MAP = MAP[:(loc1+1)] + charac + MAP[loc1+2:]
                     character[charac] = (x,y)
                     return "invalid directions provided"
       return "moved successfully"

def move(charac, command):
       global MAP
       global character
       x,y = character[charac]
       new_x, new_y = x,y
       if command == "^":
              new_x -= 1
       elif command == "v":
              new_x += 1
       elif command == ">":
              new_y += 1
       elif command == "<":
              new_y -= 1
       else:
              return 0
       if (new_x,new_y) not in location:
              return 0
       loc1 = 74*(2*x+1) + 4*y + 1
       MAP = MAP[:(loc1+1)] + " " + MAP[loc1+2:]
       loc2 = 74*(2*new_x+1) + 4*new_y + 1
       MAP = MAP[:(loc2+1)] + str(charac) + MAP[loc2+2:]
       character[charac] = (new_x,new_y)
       return 1

def show_location(x,y):
       loc = 74*(2*x+1) + 4*y + 1
       return MAP[:(loc+1)] + "X" + MAP[loc+2:]

def check_valid(x,y):
       if (x,y) in location:
              return True
       else:
              return False
def print_map():
       print(MAP)

