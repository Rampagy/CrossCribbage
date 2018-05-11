import numpy as np
import tflearn
import os

def TensorAI(board_state, card, cards_in_crib, player, crib_owner, predict_model):

    # create tf graph inputs
    observations = np.asarray(board_state).flatten().tolist() # flattened board state
    observations += [card] # drawn card
    observations += [int(player == crib_owner)] # if we own the crib
    observations += [cards_in_crib] # num of card we already put in the crib
    obs = observations

    #print(board_state)
    #print(observations)

    # convert to numpy array of floats
    observations = np.asarray(observations).reshape((1, len(observations)))

    # predict the probabilities
    probabilities = predict_model.predict(observations)
    probabilities = np.squeeze(probabilities)

    # due to rounding errors sometimes the sum will be greater than 1
    if sum(probabilities) > 1.0:
        # subtract the error from the largest probability to prevent errors
        idx = np.argmax(probabilities)
        probabilities[idx] -= sum(probabilities) - 1

    one_hot = np.random.multinomial(1, probabilities, size=1)
    move = np.argmax(one_hot)

    #print(move)

    # convert index to a board position 3='A4', 11='C2', 25='E1'
    # NOTE: the board is rotated such that the perspective is always
    # horizontal scores points, and vertical is the enemy
    # This undoes that normalization
    encoded_move = ''
    if (move == 25):
        encoded_move = 'CRIB'
    elif (player==1):
        encoded_move = chr(int(move%5)+65) + chr(int(move/5)+49)
    else: # player 0
        encoded_move = chr(int(move/5)+65) + chr(int(move%5)+49)

    #print(encoded_move)

    return obs, move, encoded_move
