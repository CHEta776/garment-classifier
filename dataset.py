import tensorflow as tf
from tensorflow import keras


def parse_function(filename):
    image_string = tf.read_file(filename)
    image = tf.image.decode_png(image_string, channels=3)
    image = 1 - tf.image.rgb_to_grayscale(image)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    image = tf.image.resize_image_with_pad(image, 28, 28)
    image.set_shape([28, 28, 1])

    return image


def load_unlabeled_data(filenames, batch_size):
    '''
    Reveices a list of filenames and returns preprocessed images as a tensorflow dataset
    :param filenames: list of file paths
    :param batch_size: mini-batch size
    :return:
    '''

    with tf.device('/cpu:0'):
        dataset = tf.data.Dataset.from_tensor_slices(filenames)
        dataset = dataset.map(parse_function, num_parallel_calls=4)
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(1)

    return dataset



def load_mnist_data(batch_size):
    train, test = keras.datasets.fashion_mnist.load_data()
    datasets = dict()

    # Create tf dataset
    with tf.device('/cpu:0'):
        with tf.variable_scope("DataPipe"):
            for data, mode in zip([train, test], ['train', 'test']):
                datasets[mode] = tf.data.Dataset.from_tensor_slices((data[0], data[1]))
                datasets[mode] = datasets[mode].map(lambda x, y: (tf.image.convert_image_dtype([x], dtype=tf.float32), tf.dtypes.cast(y, tf.int32)))
                datasets[mode] = datasets[mode].batch(batch_size=batch_size).prefetch(1)

    return datasets




