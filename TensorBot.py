from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import ParseData as pd

tf.logging.set_verbosity(tf.logging.INFO)


def cnn_model_fn(features, labels, mode):
  # Input Layer
  # Reshape X to 4-D tensor: [batch_size, width, height, channels]
  # Cribbage board is 5x5 pixels, and have one 'color channel'
  # The input is a flattened cribbage board
  input_layer = tf.reshape(features["x"], [-1, 27])

  # Dense Layer #1
  # Densely connected layer with 1024 neurons
  # Input Tensor Shape: [batch_size, 1 * 1 * 27] (27 features that are 1x1)
  # Output Tensor Shape: [batch_size, 1024]
  dense1 = tf.layers.dense(inputs=input_layer, units=1024, activation=tf.nn.relu)

  # Add dropout operation; 0.6 probability that element will be kept
  dropout1 = tf.layers.dropout(inputs=dense1, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

  # Dense Layer #2
  # Densely connected layer with 512 neurons
  # Input Tensor Shape: [batch_size, 1024]
  # Output Tensor Shape: [batch_size, 512]
  dense2 = tf.layers.dense(inputs=dropout1, units=512, activation=tf.nn.relu)

  # Add dropout operation; 0.6 probability that element will be kept
  dropout2 = tf.layers.dropout(inputs=dense2, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

  # Logits layer
  # Input Tensor Shape: [batch_size, 512]
  # Output Tensor Shape: [batch_size, 26]
  logits = tf.layers.dense(inputs=dropout2, units=26)

  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
  }
  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=26)
  loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(loss=loss,global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {"accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])}
  return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


def main(unused_argv):
  """
  # Load training and eval data
  mnist = tf.contrib.learn.datasets.load_dataset("mnist")
  train_data = mnist.train.images  # Returns np.array

  train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
  eval_data = mnist.test.images  # Returns np.array
  eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
  """

  # read in the training data
  data = pd.GetTrainingData() # Returns a np.matrix
  train_length = int(data.shape[0]*0.85)

  train_data = np.asarray(data[:train_length, :27])
  train_labels = np.asarray(data[:train_length, 27:]).flatten()

  eval_data = np.asarray(data[train_length:, :27])
  eval_labels = np.asarray(data[train_length:, 27:]).flatten()


  # Create the Estimator
  cribbage_classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir="/home/alex/models/xc_fullyconnected_model")

  # Set up logging for predictions
  # Log the values in the "Softmax" tensor with label "probabilities"
  tensors_to_log = {"probabilities": "softmax_tensor"}
  logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

  # Train the model
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": train_data},
    y=train_labels,
    batch_size=100,
    num_epochs=None,
    shuffle=True)
  cribbage_classifier.train(input_fn=train_input_fn,
    steps=40000,
    hooks=[logging_hook])

  # Evaluate the model and print results
  eval_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": eval_data},
    y=eval_labels,
    num_epochs=1,
    shuffle=False)

  eval_results = cribbage_classifier.evaluate(input_fn=eval_input_fn)
  print(eval_results)

if __name__ == "__main__":
  tf.app.run()
