"""Implementation of detection probability function layers.
"""
from keras.layers import Layer
import keras.backend as K


class EuclideanDistance(Layer):
    def __init__(self, **kwargs):
        super(EuclideanDistance, self).__init__(**kwargs)

    def build(self, input_shape):
        self.built = True

    def call(self, inputs, **kwargs):
        signals, prototypes, matrix = inputs
        signals = K.expand_dims(signals, axis=1)

        if K.shape(matrix).shape[0] > 2:
            # Tangent learning
            projected_signal_list = []
            projected_proto_list = []
            for i in range(matrix.shape[0]):
                projected_signal_list.append(K.dot(signals, matrix[i, :, :]))
                if K.shape(prototypes).shape[0] > 2:
                    current_prototypes = K.expand_dims(
                        prototypes[:, i, :], axis=1)
                    projected_proto_list.append(
                        K.dot(current_prototypes, matrix[i, :, :]))
                else:
                    current_prototypes = K.expand_dims(
                        prototypes[i, :], axis=0)
                    projected_proto_list.append(
                        K.dot(current_prototypes, matrix[i, :, :]))
            projected_prototypes = K.concatenate(projected_proto_list)
            projected_signals = K.concatenate(projected_signal_list)
            projected_signals = K.reshape(
                projected_signals,
                (K.shape(signals)[0],
                 K.shape(prototypes)[-2],
                 K.shape(matrix)[-1]))
            if K.shape(prototypes).shape[0] > 2:
                projected_prototypes = K.reshape(
                    projected_prototypes,
                    (K.shape(prototypes)[0],
                     K.shape(prototypes)[-2],
                     K.shape(matrix)[-1]))
            else:
                projected_prototypes = K.reshape(
                    projected_prototypes,
                    (K.shape(prototypes)[0],
                     K.shape(matrix)[-1]))
        else:
            # all other importances
            signals = K.tile(signals,
                             [1, K.shape(prototypes)[-2], 1])
            projected_signals = K.dot(signals, matrix)
            projected_prototypes = K.dot(prototypes, matrix)

        difference = projected_signals - projected_prototypes

        distance = K.sqrt(K.sum(K.square(difference), axis=-1))
        return distance

    def compute_output_shape(self, input_shape):
        signal_shape, prototype_shape, matrix_shape = input_shape
        n_protos = prototype_shape[1]
        return (signal_shape[0],) + (n_protos, )
