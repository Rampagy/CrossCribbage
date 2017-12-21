import numpy as np
import ComputeScore as cs

def AIBot(board_state, card, cards_in_crib, player):
    potential_grid = np.matrix([[-100, -100, -100, -100, -100],
                                [-100, -100, -100, -100, -100],
                                [-100, -100, -100, -100, -100],
                                [-100, -100, -100, -100, -100],
                                [-100, -100, -100, -100, -100]])

    temp_board_state = np.matrix([[-100, -100, -100, -100, -100],
                                  [-100, -100, -100, -100, -100],
                                  [-100, -100, -100, -100, -100],
                                  [-100, -100, -100, -100, -100],
                                  [-100, -100, -100, -100, -100]])
    
    max_potential = -100
    best_row = 0
    best_col = 0
    
    for row in range(0, len(potential_grid)):
        for column in range(0, len(potential_grid)):
            if (board_state[row, column] == 0):

                for i in range(0, len(board_state)):
                    for j in range(0, len(board_state)):
                        # reset the board state
                        temp_board_state[i, j] = board_state[i, j]
                        
                temp_board_state[row, column] = card
                
                potential = (cs.ScoreRow(temp_board_state, row) - cs.ScoreRow(board_state, row)) - \
                            (cs.ScoreRow(temp_board_state.T, column) - cs.ScoreRow(board_state.T, column))

                potential_grid[row, column] = potential
             
                if (potential > max_potential):
                    best_row = row
                    best_col = column
                    max_potential = potential

    print(potential_grid)

    # if we are player 1 going up and down swap the x and y coordinates
    if (player == 1):
        temp = best_row
        best_row = best_col
        best_col = temp

    
    if (max_potential > -1):
        return chr(best_row+65) + chr(best_col+49)
    elif (cards_in_crib < 2):
        return 'crib'
    else:
        return chr(best_row+65) + chr(best_col+49)
    
    

"""
    if (cards_in_crib < 2):
        return 'crib'
    else:
        for i in range(0, len(board_state)):
            for j in range(0, len(board_state)):
                if (board_state[i, j] == 0):
                    move = chr(i+65) + chr(j+49)
                    return move
    
    return 'no possible move'
"""

"""
self.playing_cards = {# no card
                    0: ' X ',
                    # spades
                    1:' A\u2660',
                    2:' 2\u2660',
                    3:' 3\u2660',
                    4:' 4\u2660',
                    5:' 5\u2660',
                    6:' 6\u2660',
                    7:' 7\u2660',
                    8:' 8\u2660',
                    9:' 9\u2660',
                    10:'10\u2660',
                    11:' J\u2660',
                    12:' Q\u2660',
                    13:' K\u2660',
                    # clubs
                    14:' A\u2663',
                    15:' 2\u2663',
                    16:' 3\u2663',
                    17:' 4\u2663',
                    18:' 5\u2663',
                    19:' 6\u2663',
                    20:' 7\u2663',
                    21:' 8\u2663',
                    22:' 9\u2663',
                    23:'10\u2663',
                    24:' J\u2663',
                    25:' Q\u2663',
                    26:' K\u2663',
                    # hearts
                    27:' A\u2665',
                    28:' 2\u2665',
                    29:' 3\u2665',
                    30:' 4\u2665',
                    31:' 5\u2665',
                    32:' 6\u2665',
                    33:' 7\u2665',
                    34:' 8\u2665',
                    35:' 9\u2665',
                    36:'10\u2665',
                    37:' J\u2665',
                    38:' Q\u2665',
                    39:' K\u2665',
                    # diamonds
                    40:' A\u2666',
                    41:' 2\u2666',
                    42:' 3\u2666',
                    43:' 4\u2666',
                    44:' 5\u2666',
                    45:' 6\u2666',
                    46:' 7\u2666',
                    47:' 8\u2666',
                    48:' 9\u2666',
                    49:'10\u2666',
                    50:' J\u2666',
                    51:' Q\u2666',
                    52:' K\u2666'
                    }
"""
