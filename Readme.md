# Cross Cribbage ASCII game

This game was created to provide a base for a machine learning bot to train off of.  It produces a .csv file which has a record of the moves made during the game.  The rules for the game can be [found here.](http://www.outsetmedia.com/sites/default/files/Instructions%20-%20CrossCribb.pdf)  This game will only consist of 2 player variation.

## Save format

The format the games are saved is "turn_game_state,card_being_placed,does_winner_have_crib,turn_resulting_game_state" where both game states are saved as comma seperated arrays.  The game matrix is flattened in a left to right then top to bottom fashion to form the saved array.  See example below.

This game state:

```
0,0,0,0,0
0,0,0,0,0
0,0,17,0,0
0,0,0,0,0
0,0,0,0,0
```

would be flattened to:

```
0,0,0,0,0,0,0,0,0,0,0,0,17,0,0,0,0,0,0,0,0,0,0,0,0
```

The pre-turn game state is labeled with headers "in1,in2,in3,etc..." with the last "in" being the crib.  The post-turn game state is labeled in the same way except with "out" rather than "in".

The cards are encoded into a decimal from their original hierarchy+value.  The mapping from hierarchy+value to decimal can be found in the init function of the "CribbageBoard" class.

## Artificial Intelligence

The AI currently simply goes creates a point differential grid for each position the card can be placed and then simply places it at the highest differential point.

## Two User Game

In order to play with a User vs AI rather than AI vs AI, simply replace comment line 39 and uncomment line 40 and 41 in CrossCribbage.py as shown below.

AI vs AI

```python
move = aib.AIBot(board.GetBoardState().transpose(), card, board.GetCardsInCrib(1), 1)
#print(board.DecipherCard(card))
#move = ub.UserBot(board.GetBoardState(), card, board.GetCardsInCrib(1))
```

AI vs User

```python
#move = aib.AIBot(board.GetBoardState().transpose(), card, board.GetCardsInCrib(1), 1)
print(board.DecipherCard(card))
move = ub.UserBot(board.GetBoardState(), card, board.GetCardsInCrib(1))
```