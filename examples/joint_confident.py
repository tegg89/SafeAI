# Copyright (c) 2018 Episys Science, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import numpy as np
import tensorflow as tf
from safeai.models.joint_confident import confident_classifier
tf.logging.set_verbosity(tf.logging.INFO)
mnist = tf.keras.datasets.mnist


def dcgan_discriminator():
    """
    docstring
    """
    pass


def dcgan_generator():
    """
    docstring
    """
    pass


def vgg_classifier():
    # from tensorflow.contrib.slim.nets import vgg16
    """
    docstring
    """
    pass


def train_input_fn(features, labels, noise_size, batch_size):
    """
    docstring
    """
    noise = np.random.random((features.shape[0], noise_size))
    dataset = tf.data.Dataset.from_tensor_slices(
            ({'image': features, 'noise': noise}, labels)
    )
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset


def eval_input_fn(features, labels, noise_size, batch_size):
    """
    Used in both evaluation, prediction
    """
    noise = np.random.random((features.shape[0], noise_size))
    features_dict = {'image': features, 'noise': noise}
    if labels is None:
        inputs = features_dict
    else:
        inputs = (features_dict, labels)

    dataset = tf.data.Dataset.from_tensor_slices(inputs).batch(batch_size)
    return dataset


def main():
    """
    docstring
    """
    batch_size = 256
    train_steps = 10000
    noise_dim = 100
    num_classes = 10
    image_dim = (28, 28)
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train/255., x_test/255.
    # Todo: one-hot Tue 06 Nov 2018 09:36:29 PM KST
    image_width, image_height = x_train.shape[1:]

    image_feature = tf.feature_column.numeric_column(
            'image', shape=(image_width, image_height))
    noise_feature = tf.feature_column.numeric_column('noise', shape=noise_dim)

    # Todo: Reduce params['dim'] Tue 06 Nov 2018 05:05:10 PM KST
    joint_confident_classifier = tf.estimator.Estimator(
        model_fn=confident_classifier,
        params={
            'image': [image_feature],
            'noise': [noise_feature],
            'image_dim': image_dim,
            'noise_dim': noise_dim,
            'num_classes': num_classes,
            'discriminator': None,
            'generator': None,
            'classifier': None,
            'learning_rate': 0.001,
            'beta': 1.0,
        })

    joint_confident_classifier.train(
        input_fn=lambda: train_input_fn(x_train, y_train,
                                        noise_dim, batch_size),
        steps=train_steps
    )

    eval_result = joint_confident_classifier.evaluate(
        input_fn=lambda: eval_input_fn(x_test, y_test, noise_dim, batch_size),
        steps=train_steps
    )
    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


if __name__ == "__main__":
    main()
