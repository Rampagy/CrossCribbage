import numpy as np
import TensorBot as tb
import tensorflow as tf
import os

def TensorAI(board_state, card, cards_in_crib, player, crib_owner):
    model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cx_fullyconnected_model', 'model.ckpt')

    # build your model (same as training)
    """
    sess = tf.Session()
    saver = tf.train.Saver()
    saver.restore(sess, model_path)

    print(temp_board_state)
    print(type(temp_board_state[0]))
    """

    temp_board_state = np.asarray(board_state).flatten().tolist()
    temp_board_state += [card]
    temp_board_state += [int(player == crib_owner)]
    temp_board_state = np.float32(np.asarray(list(map(float, temp_board_state))))

    # Create the Estimator
    cribbage_classifier = tf.estimator.Estimator(model_fn=tb.cnn_model_fn, model_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "xc_fullyconnected_model"))

    # Evaluate the model and print results
    pred_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": temp_board_state},
      num_epochs=1,
      shuffle=False)

    eval_results = cribbage_classifier.predict(input_fn=pred_input_fn)
    position_probabilities = next(eval_results)['probabilities']

    temp_board = np.asarray(board_state).flatten()

    max_prob = 0.0
    best_pos = 0

    for i in range(0, len(position_probabilities)):
        # if the best position is the crib
        if ((position_probabilities[i] > max_prob) and (i==25)):
            # and the crib has open spots
            if (cards_in_crib < 2):
                max_prob = position_probabilities[i]
                best_pos = i
            else:
                continue
        # if the best position doesn't already have a card there
        elif (position_probabilities[i] > max_prob) and (temp_board[i] == 0):
            max_prob = position_probabilities[i]
            best_pos = i

    move = ''
    if (best_pos == 25):
        move = 'CRIB'
    elif (player==1):
        move = chr(int(best_pos%5)+65) + chr(int(best_pos/5)+49)
    else: # player 0
        move = chr(int(best_pos/5)+65) + chr(int(best_pos%5)+49)

    print(move)



















def a():
    pass
