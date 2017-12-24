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
    temp_board_state = list(map(float, temp_board_state))

    # Create the Estimator
    cribbage_classifier = tf.estimator.Estimator(model_fn=tb.cnn_model_fn, model_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "xc_fullyconnected_model"))

    # Set up logging for predictions
    # Log the values in the "Softmax" tensor with label "probabilities"
    #tensors_to_log = {"probabilities": "softmax_tensor"}
    #logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    # Evaluate the model and print results
    pred_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": temp_board_state},
      y=0,
      num_epochs=1,
      shuffle=False)

    eval_results = cribbage_classifier.predict(input_fn=pred_input_fn)
    print(eval_results)
    take(26, eval_results)
