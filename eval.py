import tensorflow as tf
from dataset import load_unlabeled_data
from utils import get_files, label_dict
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd


# Params from model to recover
tf.flags.DEFINE_string('model_dir', 'Models/', 'Saved model directory')
tf.flags.DEFINE_string('model_description', 'garment_classifier', 'Model name')
tf.flags.DEFINE_string('data_path', 'Data/Images', 'Images folder path')
tf.flags.DEFINE_integer('batch_size', 5, 'Minibatch size')


FLAGS = tf.flags.FLAGS

# Create graph
graph = tf.Graph()

# Restore network
with tf.Session(graph=graph) as sess:
    # Prepare data to predict
    filenames = get_files(FLAGS.data_path)
    dataset = load_unlabeled_data(filenames, FLAGS.batch_size)
    iterator = dataset.make_initializable_iterator()
    input_batch = iterator.get_next()
    saver = tf.train.import_meta_graph(FLAGS.model_dir+'{}.meta'.format(FLAGS.model_description))
    saver.restore(sess, tf.train.latest_checkpoint(FLAGS.model_dir))

    # Recover tensors and ops from graph
    input_data = graph.get_tensor_by_name('DataPipe/input_data:0')
    prediction = graph.get_tensor_by_name('Network/output_class:0')

    sess.run(iterator.initializer)

    # Simple test to show results
    f, axarr = plt.subplots(1,5)
    images = sess.run(input_batch)
    labels = sess.run(prediction, feed_dict={input_data: images})

    for i in range(5):
        img = mpimg.imread(filenames[i])
        axarr[i].imshow(img)
        axarr[i].axis('off')
        axarr[i].set_title(label_dict[labels[i]])
    plt.show()


    # Tag the whole dataset
    predicted_labels = []
    sess.run(iterator.initializer)

    while True:
        try:
            images = sess.run(input_batch)
            labels = sess.run(prediction, feed_dict={input_data: images})
            predicted_labels.append(labels)

        except tf.errors.OutOfRangeError:
            break
    predicted_labels = [label_dict[i] for i in np.concatenate(predicted_labels)]

    labeled_data = pd.DataFrame({'filenames': filenames, 'labels': predicted_labels})
    labeled_data.to_csv('labeled_data.csv')
