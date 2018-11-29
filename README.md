# halliganClue
A Halligan-themed Clue game

## Instructions
Run ./test in a terminal window with forwarding enabled to automatically create three clients (all client objects called "c").


## Notes
raw_input blocks receiving - use curses to fix this?
Just using the name thing to test notifications.


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
