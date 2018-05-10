import CrossCribbage as xc
import tflearn
import tensorflow as tf
import numpy as np
import os



# OPTION PARAMETERS
# tensorboard name
tb_name = 'tensorboard'
# file dir for saving the model
save_loc = './model'
# model checkpoint filename
chkpnt_name = 'model.ckpt'
# number of games to play
n_game = 10000000
# intervals between saves
checkpoint_interval = 1000
# if testing
TEST = False



# function to create tensorflow model
def create_model():
    network = tflearn.input_data(shape=[None, 28], name='input')
    network = tflearn.fully_connected(network, 127, activation='relu')
    network = tflearn.dropout(network, 0.3) # 0.3 = keep prob
    network = tflearn.fully_connected(network, 127, activation='relu')
    network = tflearn.dropout(network, 0.3) # 0.3 = keep prob
    network = tflearn.fully_connected(network, 127, activation='relu')
    network = tflearn.dropout(network, 0.3) # 0.3 = keep prob
    network = tflearn.fully_connected(network, 26, activation='softmax')
    network = tflearn.regression(network, optimizer='adam', learning_rate=0.000005,
                         loss='binary_crossentropy', name='target', metric=None)

    model = tflearn.DNN(network, tensorboard_verbose=0, tensorboard_dir=save_loc)

    # load saved weights if possible
    if tf.train.latest_checkpoint(save_loc) != None:
        model.load(os.path.join(save_loc, chkpnt_name))
        print('load')
    else:  # else init the weights
        init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        model.session.run(init)
        print('init')

    return model, network


def conv_trainable_data(win_log, lose_log):
    # convert to numpy array to matrix operations
    win_log = np.asarray(win_log)
    lose_log = np.asarray(lose_log)

    # encourage the winning moves
    win_move = win_log[:, 1]
    win_label = tflearn.data_utils.to_categorical(win_move, 26)

    # discourage the losing moves
    lose_move = lose_log[:, 1]
    lose_label = np.logical_not(tflearn.data_utils.to_categorical(lose_move, 26))
    lose_label = lose_label*1.0

    # combine into one matrix
    labels = np.append(win_label, lose_label, axis=0)

    # gather observations/features
    win_feat = win_log[:, 0].tolist()
    lose_feat = lose_log[:, 0].tolist()

    # combine into one matrix
    features = np.append(win_feat, lose_feat, axis=0)

    return features, labels




if __name__ == '__main__':
    # create the model
    model, network = create_model()

    if not TEST:
        # play the game X times
        for i in range(0, n_game):
            win_log, lose_log = xc.PlayGame(model)

            # only train if there is data in both the in and lose log
            if np.asarray(win_log).shape[0]>=1 and np.asarray(lose_log).shape[0]>=1:
                # parse the logs for trainable data
                features, labels = conv_trainable_data(win_log, lose_log)

                # train based on the trainable data
                model.fit({'input': features}, {'target': labels}, n_epoch=4,
                        show_metric=False, batch_size=500, shuffle=True, run_id=tb_name)

            if i % checkpoint_interval == 0:
                model.save(os.path.join(save_loc, chkpnt_name))

            print(i)
    else:
        # test the AI
        xc.PlayGame(model, GraphicsOn=True, Test=TEST)
