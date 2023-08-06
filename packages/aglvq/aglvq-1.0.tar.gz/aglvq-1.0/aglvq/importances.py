# Imports
from .input_layer import ConstantInput, AddComponents
from .constraints import Relevance_Normalization, Normalization, Orthogonalization
from .layers import Prepare_Tangents
from .initializer import PCA_Initializer

import numpy as np
from keras.layers import Lambda
import keras.backend as K
from keras.initializers import Identity, Ones


# Class definition
class Imp():

    def __init__(self,
                 shape,
                 n_tangents,
                 n_protos,
                 pca_data,
                 imptype='none'):
        self.shape = shape[0]
        self.n_tangents = n_tangents
        self.n_protos = n_protos
        if pca_data is not None:
            self.tangent_initializer = PCA_Initializer(pca_data)
        else:
            self.tangent_initializer = Ones()
        if imptype == 'none':
            self.imp_input, self.importances = self._imp_const()
        if imptype == 'relevance':
            self.imp_input, self.importances = self._imp_relevance()
        if imptype == 'matrix':
            self.imp_input, self.importances = self._imp_matrix()
        if imptype == 'tangent':
            self.imp_input, self.importances = self._imp_tangent()

    def _imp_const(self):
        const_input = ConstantInput(np.zeros((1,)), name='constant_imp')()
        add_components = AddComponents(shape=(self.shape, self.shape),
                                       name='ones', trainable=False,
                                       initializer=Identity()
                                       )
        importances = add_components(const_input)

        return const_input, importances

    def _imp_relevance(self):
        const_input = ConstantInput(np.zeros((1,)), name='relevance_imp')()
        add_components = AddComponents(shape=(self.shape,),
                                       name='importance',
                                       constraint=Relevance_Normalization(),
                                       initializer='ones')
        imp_vector = add_components(const_input)
        importances = Lambda(lambda x: K.eye(K.shape(x)[0]) * x)(imp_vector)
        return const_input, importances

    def _imp_matrix(self):
        const_input = ConstantInput(np.zeros((1,)), name='matrix_imp')()
        add_components = AddComponents(shape=(self.shape, self.shape),
                                       name='importance',
                                       constraint=Normalization(),
                                       initializer=Identity())
        importances = add_components(const_input)
        return const_input, importances

    def _imp_tangent(self):
        const_input = ConstantInput(np.zeros((1,)), name='matrix_imp')()
        add_components = AddComponents(
            shape=(self.n_protos, self.shape, self.n_tangents),
            name='importance',
            constraint=Orthogonalization(),
            initializer=self.tangent_initializer)
        tangent_vector = add_components(const_input)
        importances = Prepare_Tangents(
            n_protos=self.n_protos, signal_shape=self.shape)(tangent_vector)
        return const_input, importances
