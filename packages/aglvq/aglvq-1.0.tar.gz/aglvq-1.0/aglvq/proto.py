# Imports
from keras.layers import Add, Input, Dense, BatchNormalization, Reshape
from keras.regularizers import l2
from keras.models import Model
from keras.initializers import Zeros

from .layers import Polynomial, ProtoAdd
from .input_layer import ConstantInput, AddComponents
from .initializer import Mean_Initializer

import numpy as np


# Class definition
class proto():

    def __init__(self,
                 env_shape,
                 reg_rate,
                 n_poly,
                 init_values,
                 n_prototypes,
                 ptype='const',
                 prototype_shape=None):
        self.n_prototypes = n_prototypes
        self.prototype_shape = prototype_shape
        self.reg_rate = reg_rate
        self.n_poly = n_poly
        if init_values is not None:
            self.proto_initializer = Mean_Initializer(init_values)
        else:
            self.proto_initializer = Zeros()

        if ptype == 'const':
            self.env, self.prototypes, self.model = self._init_proto_const()

        if ptype == 'polynom' or ptype == 'neural' or ptype == 'simple_neural':
            if env_shape is not None:
                self.env_shape = env_shape
            else:
                raise Exception('Polynom and neural Network prototype path requires input')
            self.env, self.prototypes, self.model = self._proto_combined(ptype)

    def _init_proto_const(self):
        env = ConstantInput(np.zeros((1,)), name='constant')()
        add_components = AddComponents(shape=(self.n_prototypes,)
                                       + self.prototype_shape,
                                       name='prototypes_constant',
                                       initializer=self.proto_initializer)
        protos = add_components(env)
        model = Model(env, protos)
        return [env], protos, model

    def generate_proto(self, env):
        return self.model.predict(env)

    def _proto_combined(self, comb_type):
        if comb_type == 'polynom':
            env, c = self._polynom_path(self.n_poly)
        if comb_type == 'neural':
            env, c = self._neural_path()
        if comb_type == 'simple_neural':
            env, c = self._simple_neural_path()
        env_const, protos_const, _ = self._init_proto_const()
        protos_added = ProtoAdd(name='prototypes')([c, protos_const])
        model = Model(env + env_const, protos_added)
        return env + env_const, protos_added, model

    def _polynom_path(self, n_poly=2):
        env = Input(shape=self.env_shape)
        c_poly = []
        for i in range(n_poly):
            c = Polynomial(neurons=self.n_prototypes*self.prototype_shape[0],
                           power=i+1, regularizer=l2(self.reg_rate))(env)
            c_poly.append(c)
        c = Add()(c_poly)
        c = Reshape((self.n_prototypes,) + self.prototype_shape)(c)

        return [env], c

    def _neural_path(self):
        env = Input(shape=self.env_shape, name='c_Input')
        c = Dense(32, activation='relu',
                  kernel_regularizer=l2(self.reg_rate))(env)
        c = BatchNormalization(name='BatchNormalization_01')(c)
        c = Dense(32, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_01')(c)
        c = BatchNormalization(name='BatchNormalization_02')(c)
        c = Dense(64, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_02')(c)
        c = BatchNormalization(name='BatchNormalization_03')(c)
        c = Dense(64, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_03')(c)
        c = BatchNormalization(name='BatchNormalization_04')(c)
        c = Dense(64, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_04')(c)
        c = BatchNormalization(name='BatchNormalization_05')(c)
        c = Dense(96, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_05')(c)
        c = BatchNormalization(name='BatchNormalization_06')(c)
        c = Dense(96, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_06')(c)
        c = BatchNormalization(name='BatchNormalization_07')(c)
        c = Dense(128, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_07')(c)
        c = BatchNormalization(name='BatchNormalization_08')(c)
        c = Dense(128, activation='relu', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_08')(c)
        c = BatchNormalization(name='BatchNormalization_09')(c)
        c = Dense(self.n_prototypes*self.prototype_shape[0],
                  kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_09')(c)
        c = Reshape((self.n_prototypes,) + self.prototype_shape,
                    name='ReshapeLayer')(c)
        return [env], c

    def _simple_neural_path(self):
        env = Input(shape=self.env_shape, name='c_Input')
        c = Dense(100, activation='tanh',
                  kernel_regularizer=l2(self.reg_rate))(env)
        c = Dense(100, activation='tanh', kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_01')(c)
        c = Dense(self.n_prototypes*self.prototype_shape[0],
                  kernel_regularizer=l2(self.reg_rate),
                  name='Fully_Connected_Layer_02')(c)
        c = Reshape((self.n_prototypes,) + self.prototype_shape,
                    name='ReshapeLayer')(c)
        return [env], c
