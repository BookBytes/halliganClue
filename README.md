# halliganClue
A Halligan-themed Clue game

## Instructions
Run ./test in a terminal window with forwarding enabled to automatically create three clients (all client objects called "c").


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
