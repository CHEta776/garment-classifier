from network import Network
import tensorflow as tf
from dataset import load_mnist_data
import os
from utils import create_folder, delete_old_logs, create_results_folder
from time import time

# Program parameters
tf.flags.DEFINE_float('learning_rate', .0001, 'Initial learning rate.')
tf.flags.DEFINE_integer('epochs', 100, 'Number of steps to run trainer.')
tf.flags.DEFINE_integer('batch_size', 128, 'Minibatch size')
tf.flags.DEFINE_integer('latent_dim', 2, 'Number of latent dimensions')
tf.flags.DEFINE_integer('test_image_number', 5, 'Number of test images to recover during training')
tf.flags.DEFINE_integer('epochs_to_plot', 2, 'Number of epochs before saving test sample of reconstructed images')
tf.flags.DEFINE_integer('validation_after_n', 2, 'Number of epochs before apply validation testing')
tf.flags.DEFINE_integer('save_after_n', 2, 'Number of epochs before saving network')
tf.flags.DEFINE_string('logdir', './logs', 'Logs folder')
tf.flags.DEFINE_string('data_path', './Data/Images', 'Logs folder')
tf.flags.DEFINE_string('model_description', 'garment_classifier', 'Model name')
tf.flags.DEFINE_bool('shuffle', True, 'Shuffle dataset for training')
FLAGS = tf.flags.FLAGS


# Prepare output directories
results_folder = create_results_folder(os.path.join('Results', FLAGS.model_description))
model_folder = create_folder(os.path.join('Models', FLAGS.model_description))
delete_old_logs(FLAGS.logdir)


# Create tf dataset
with tf.name_scope('DataPipe'):
    datasets = load_mnist_data(FLAGS.batch_size)
    iterator = tf.data.Iterator.from_structure(datasets['train'].output_types,
                                           datasets['train'].output_shapes)

    # create the initialisation operations
    train_init_op = iterator.make_initializer(datasets['train'])
    test_init_op = iterator.make_initializer(datasets['test'])

    input_batch, labels = iterator.get_next()
    input_batch = tf.reshape(input_batch, shape=[-1, 28, 28, 1])
    input_data = tf.placeholder_with_default(input_batch, [None, 28, 28, 1], name='input_data')

# Create model
is_training = tf.placeholder_with_default(True, (), name='is_traning')

model = Network(input_data, labels, FLAGS.learning_rate, is_training )

# Get metrics variables to be reset after each epoch
metrics = tf.get_collection(tf.GraphKeys.LOCAL_VARIABLES, scope="metrics/*")
reset_metrics = tf.variables_initializer(var_list=metrics)


init_vars = [tf.local_variables_initializer(), tf.global_variables_initializer()]
saver = tf.train.Saver()

# Training loop
with tf.Session() as sess:
    writer = tf.summary.FileWriter('./logs', sess.graph)

    sess.run(init_vars)
    merged_summary_op = tf.summary.merge_all()

    for epoch in range(FLAGS.epochs):
        print('Actual epochs is: {}'.format(epoch), end='', flush=True)
        sess.run(train_init_op)
        flag = True
        ts = time()

        # Training loop
        while True:
            try:
                sess.run(model.optimize)

            except tf.errors.OutOfRangeError:
                print('\t Epoch time: {}'.format(time() - ts))
                break

        # Validation loop
        if not epoch % FLAGS.validation_after_n:
            sess.run(test_init_op)

            while True:
                try:
                    sess.run(model.accuracy)
                    test_summaries, acc = sess.run([merged_summary_op, model.accuracy], feed_dict={is_training: False})

                except tf.errors.OutOfRangeError:
                    writer.add_summary(test_summaries, epoch)
                    print('Validation time: {}'.format(time() - ts))
                    sess.run([reset_metrics])
                    break

        # Save model
        if not epoch % FLAGS.save_after_n:
            print('Saving model...')
            saver.save(sess, model_folder)
