import numpy as np

# AI bot always goes left and right

def AIBot(board_state, card, cards_in_crib):    
    if (cards_in_crib < 2):
        return 'crib'
    else:
        for i in range(0, len(board_state)):
            for j in range(0, len(board_state)):
                if (board_state[i, j] == 0):
                    move = chr(i+65) + chr(j+49)
                    return move
    
    return 'no possible move'
