# Imports
from keras.layers import Layer
import keras.backend as K


class Softmin(Layer):
    """
    Custom Softmin function to convert distances into softmax-probabilities
    """

    def __init__(self, factor, **kwargs):
        self.factor = factor
        super(Softmin, self).__init__(**kwargs)

    def call(self, inputs):
        diss = inputs
        diss = diss * (-1) * self.factor
        output = K.softmax(diss, axis=-1)
        return output


class Squeezze(Layer):
    """
    Returns the matching prototype
    """

    def __init__(self, **kwargs):
        super(Squeezze, self).__init__(**kwargs)

    def call(self, inputs):
        labels = inputs[0]
        prototypes = inputs[1]
        labels = K.expand_dims(labels, -1)
        masked = labels * prototypes
        output = K.sum(masked, axis=1)
        return output

    def compute_output_shape(self, input_shape):
        return (input_shape[1][0], input_shape[1][-1])


class ProtoAdd(Layer):
    def __init__(self, **kwargs):
        super(ProtoAdd, self).__init__(**kwargs)

    def call(self, inputs):
        can_data, protos = inputs
        protos = K.expand_dims(protos, 0)
        protos = K.tile(protos, [K.shape(can_data)[0], 1, 1])
        protos_added = protos + can_data
        return protos_added

    def compute_output_shape(self, input_shape):
        can_data_shape, proto_shape = input_shape
        return can_data_shape


class Polynomial(Layer):
    def __init__(self, neurons, power, regularizer=None, **kwargs):
        self.power = power
        self.neurons = neurons
        self.regularizer = regularizer
        super(Polynomial, self).__init__(**kwargs)

    def build(self, input_shape):
        self.w = self.add_weight(name='factor', shape=(self.neurons,),
                                 initializer='zeros',
                                 regularizer=self.regularizer)
        self.b = self.add_weight(name='bias', shape=(self.neurons,),
                                 initializer='zeros',
                                 regularizer=self.regularizer)
        self.built = True

    def call(self, inputs):
        return self.w * (inputs**self.power) + self.b

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.neurons)


class Prepare_Tangents(Layer):
    def __init__(self, n_protos, signal_shape, **kwargs):
        self.n_protos = n_protos
        self.signal_shape = signal_shape
        super(Prepare_Tangents, self).__init__(**kwargs)

    def call(self, inputs):
        x = inputs
        importances_list = []
        for i in range(self.n_protos):
            importances_list.append(
                K.eye(K.shape(x[i, :, :])[0]) - K.dot(x[i, :, :], K.transpose(x[i, :, :])))
        importances = importances_list[0]
        importances = K.expand_dims(importances, axis=0)
        importances = K.concatenate((importances, importances_list[1:]), axis=0)
        return importances

    def compute_output_shape(self, input_shape):
        return (self.n_protos, self.signal_shape, self.signal_shape)
