# halliganClue
A Halligan-themed Clue game

## Instructions
To run HalliganClue quickly use our test script.
Note that all ‘users’ are running on the same device so this is
a single user acting as all players. The command to run the
script is as follows. Make sure x11-forwarding is enabled:

./test

The server will pop up first with an address for the clients to
join (manually). After that simply follow the prompts and solve the murder!

To run the game with all unique users (aka multiple) run:
python server.py
python client.py
python client.py
python client.py

Each of these commands must be run in a separate terminal with a
separate ssh session into the homework server. This way you'll
end up on a different computer each time.

## File Overview
client.py:
Code for client side interactions such as terminal interactions
and message passing to the server.

server.py
Code for starting a server and starting up games when a sufficient
number of clients have connected.

client_handler.py
Code for receiving client messages, run on a thread per client by
the server. Contains logic for how to process each message type.

contacts.py
Class for holding address and game order information, used by code
in client_handler.py to send messages to the various clients in a game.

game.py 
Classes for game logic and object representation of game components,
including Elements, Suspects, and Weapons, including logic for valid
actions with sanity checks

map.py
Contains board representation and location and map-related logic, as
well as marked key locations

game_data.py 
Contains game data that would have cluttered up other files like
character/action/places/action enumerations and key-mappings.

message.py
Contains enumeration for each message type with comments on their use
and a Message class that encodes/decodes messages to be passed between
client and server and can pretty-print the message. Also contains a
helper function that takes a socket and returns a Message object so
that the client/server do not have to worry about the format by which
message size is passed.


We kept our initial prototype tests in the tests folder for any
needed experimentation.

As well we created two test scripts (‘test’ for the homework server
and ‘localtest’ for Ubuntu Linux - Juliana's local development
environment). These test scripts start a server and open up enough
clients to start a game. This quick-starts the game process and was
helpful for testing purposes.

We used only the built-in Python library so the entirety of the code is our own.


## Would be nice
- Notify everyone turn is being taken
- Better ordering of player
- Game end request
- Block the door
- Fix passageways, movements
- Add message for early start to allow games of varying player group size (2-6), starts automatically at 6


roll, passage
        roll
return number w/ move prompt
        move string
accept move string
send msg
send new map
if applicable, offer suggestion prompt
        make suggestion
begin suggestion logic
        offer accuse at the end

game -> available actions

### An ideal list of messages
##### Client <-> Server

* Join (name)->
    * <- Join Notification (All)
* Character list request ->
    * <- Available Characters
* Character request ->
    * <- Confirmation OR character list if choice taken
    * <- Deck


(Weapon placement stage)

* Dice roll (ordering) ->
    * <- Order info (all)
    * <- Turn request

Take turn:
* Move request ->
    * <- Map update (all) or rejection w/ reason (+ ideally a confirmation here)
* Suggestion (only if in room) ->
    * <- Map update (all), suggestion rebuttal request (next player)
* Suggestion rebuttal or pass ->
    * <- Rebuttal info or nothing (OG player)
    * <- Rebuttal notification (all)


* leave ->
    * <- Graceful exit (all)
