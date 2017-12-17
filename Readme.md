# Cross Cribbage ASCII game

This game was created to provide a base for a machine learning bot to train off of.  
It produces a .xcb file which has a record of the moves made during the game.  The 
rules for the game can be [found here.](http://www.outsetmedia.com/sites/default/files/Instructions%20-%20CrossCribb.pdf)  
This game will only consist of 2 player variation.

## Save format

The 'x' in xcb stands for 'cross' and 'cb' stands for 'cribbage'.  The format for each
of line is as such 'TurnNumber:Player:Card:Position'. An example line from an .xcb 
is shown below:

> 1:1:28:C3
> 2:0:13:crib
> 3:0:1:crib
> 4:0:50:A1

The first line means that on the 1st turn player 1 moved card 28 to position C2.  The 
second line means on turn 2 player 0 moved card 13 to the crib.  The third line means 
on turn 3 player 0 moved card 1 to the crib.  The last line means on turn 4 player 0 
moved card 50 to A1.

## Artificial Intelligence

Currently the AI simply goes from left to right then top to bottom unless his crib is 
not filled.  In the future this may change.  This Ai was made simply so that you could 
have someone to play against and record .xcb files for a Convolution Neural Network to
be trained.

## Two User Game

In order to play with two Users rather than one AI and one user, simply replace
'move = aib.AIBot(board.GetBoardState(), card, board.GetCardsInCrib(0))' with 
'print(board.DecipherCard(card))
move = ub.UserBot(board.GetBoardState(), card, board.GetCardsInCrib(1))' in 
'PlayCrossCribbage.py'.