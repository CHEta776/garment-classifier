import tensorflow as tf
import functools



def define_scope(function):
    # Decorator to lazy loading from https://danijar.com/structuring-your-tensorflow-models/
    attribute = '_cache_' + function.__name__
    @property
    @functools.wraps(function)
    def decorator(self):
        if not hasattr(self, attribute):
                setattr(self, attribute, function(self))
        return getattr(self, attribute)

    return decorator


class Network:

    def __init__(self, data, labels, learning_rate, is_training):
        self.data = data
        self.labels = labels
        self.learning_rate = learning_rate
        self.is_training = is_training
        self.forward_pass
        self.optimize
        self.accuracy


    @define_scope
    def forward_pass(self):
        activation = tf.nn.relu
        with tf.variable_scope('Data'):
            x = self.data
        with tf.variable_scope('Network'):
            x = tf.layers.conv2d(x, filters=64, kernel_size=5, padding='same', activation=activation)
            x = tf.layers.max_pooling2d(inputs=x, pool_size=[2, 2], strides=2)

            x = tf.layers.conv2d(x, filters=64, kernel_size=5, padding='same', activation=activation)
            x = tf.layers.max_pooling2d(inputs=x, pool_size=[2, 2], strides=2)

            x = tf.layers.flatten(x)

            # Local latent variables
            x = tf.layers.dense(x, units=1024, activation=activation)
            x = tf.layers.dropout(inputs=x, rate=0.4, training=self.is_training)

            self.logits = tf.layers.dense(inputs=x, units=10)

            predictions = {
                'classes': tf.argmax(input=self.logits, axis=1, name='output_class'),
                'probabilities': tf.nn.softmax(self.logits, name='softmax_tensor')
            }

            return predictions


    @define_scope
    def optimize(self):
        with tf.variable_scope('Optimize'):
            loss = tf.losses.sparse_softmax_cross_entropy(labels=self.labels, logits=self.logits)
            optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(loss)
            tf.summary.scalar('batch_loss', loss)
        return optimizer


    @define_scope
    def accuracy(self):
        with tf.name_scope('Metrics'):
            _, update_acc = tf.metrics.accuracy(self.forward_pass['classes'], self.labels, name="accuracy")
        tf.summary.scalar('epoch_accuracy', update_acc)
        return update_acc
