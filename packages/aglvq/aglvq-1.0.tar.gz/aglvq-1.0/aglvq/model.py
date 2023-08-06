# Own Imports
from .proto import proto
from .importances import Imp
from .distance import EuclideanDistance
from .losses import glvq_swish_loss as glvq_loss
from .layers import Softmin, Squeezze
from . import plotting

# Other imports
from keras.models import Model
from keras.layers import Input
from keras.optimizers import RMSprop
from keras.metrics import categorical_accuracy
from keras.utils import plot_model
from sklearn.decomposition import PCA
import numpy as np
import json
import os


# Accuracy metric for glvq loss
def accuracy(y_true, y_pred):
    return categorical_accuracy(y_true, -y_pred)


# Class definition
class Alvq_Model():
    """
    Create ALVQ model

    Parameters
    ----------
    n_classes : int
        Number of Classes.
    ptype : TYPE, optional
        Type of prototypes:
            'const': static prototypes,
            'polynom': Prototypes with polynomial path,
            'neural': Prototypes with neural network path.
            The default is 'const'.
    imptype : TYPE, optional
        Type of importances:
            'none': No importances (=GLVQ)
            'relevance': Relevance vector (=GRLVQ),
            'matrix': Importance matrix (=GRLVQ)
            'tangent': Orthoprojector matrix (=GTLVQ).
            The default is 'none'.
    opt : TYPE, optional
        Optimizer. The default is None.
    learning_rate : float, optional
        Learning rate
        Some guidelines for more difficult learning problems:
        'const': 1e-3,
        'polynom': 2e-6,
        'neural': 4e-6. The default is 0.01.
    pre_train_lr : TYPE, optional
        Learning rate for pretraining. The default is 0.01.
    prototype_shape : tuple, optional
        Shape of Prototypes. The default is None.
    env_shape : tuple, optional
        Shape of environment factor. The default is None.
    reg_rate : float, optional
        Regularisation rate for l2 regularizer
        Some guidlines:
        'const': 0,
        'polynom': 0,
        'neural': 3e-5. The default is 0.
    n_poly : int, optional
        Max power of polynom path. The default is 2.
    aux_factor : float, optional
        Factor for auxillary loss [0,1]. The default is 0.
    distance_factor : float, optional
        Factor for distance loss [0,1]. The defualt is 1.0.
    initializing_data: list, optional
        List of X and Y data for initialization of prototypes.
        The default is None.
    pre_training: bool, optional
        Enables or disables pre training. The default is True.
    n_tangents: int, optional
        Number of tangent subspaces fot GTLVQ. The default is 10.
    softmin_factor: int, optional
        Scaling factor for the Softmin Layer. The default is 1.

    Returns
    -------
    None.

    """

    def __init__(self,
                 n_classes,
                 ptype='const',
                 imptype='none',
                 opt=None,
                 learning_rate=0.01,
                 pre_train_lr=0.01,
                 prototype_shape=None,
                 env_shape=None,
                 reg_rate=0,
                 n_poly=2,
                 aux_factor=0,
                 distance_factor=1,
                 initialize_data=None,
                 pre_training=True,
                 n_tangents=10,
                 pca_init=True,
                 proto_mean_init=True,
                 softmin_factor=1):

        # Properties
        self.env_shape = env_shape
        self.reg_rate = reg_rate
        self.input_shape = prototype_shape
        self.lr = learning_rate
        self.pre_train_lr = pre_train_lr
        self.ptype = self._init_ptype(ptype)
        self.n_classes = n_classes
        self.n_poly = n_poly
        self.n_tangents = n_tangents
        self.imptype = imptype
        self.opt = self._init_opt(opt)
        self.prototypes = None
        self.importances = None
        self.input = None
        self.aux_factor = aux_factor
        self.distance_factor = distance_factor
        self.enable_pre_train = pre_training
        if prototype_shape is not None:
            self.prototype_shape = prototype_shape
        else:
            raise Exception('Prototype Shape has to be provided')
        if initialize_data is not None:
            if proto_mean_init:
                self.mean_data = self._init_means(initialize_data)
            else:
                self.mean_data = None
            if pca_init:
                self.pca_data = self._init_pca(initialize_data)
            else:
                self.pca_data = None

        else:
            self.mean_data = None
            self.pca_data = None
        self.softmin_factor = softmin_factor

        # Initialize Model
        self.model = self._init_model()
        self.prediction_model = self._init_prediction_model()
        self.pre_train_model = self._init_pre_train_model()
        if aux_factor > 0:
            self.aux_model = self._init_aux_loss_model()

        # Inititalize directories
        self._init_folder_structure()

    def _init_folder_structure(self):
        # Folder for saving models
        model_dir = os.path.dirname(__file__)
        if not os.path.exists(model_dir + '/models/'):
            os.makedirs(model_dir + '/models/')
        # Folder for figures
        current_dir = os.getcwd()
        if not os.path.exists(current_dir + '/figures/'):
            os.makedirs(current_dir + '/figures/')

    def _init_model(self):
        # Inititalise parts of the model
        self.prototypes = self._init_proto_model()
        self.importances = self._init_imp_model()
        self.input = Input(self.input_shape)

        self.distances = EuclideanDistance(name='distance')(
            [self.input,
             self.prototypes.prototypes,
             self.importances.importances])
        # Build mdoel
        input_list = [self.input] + self.prototypes.env + \
            [self.importances.imp_input]
        model = Model(input_list, self.distances)
        model = self._compile_model(model)
        return model

    def _compile_model(self, model):
        model.compile(optimizer=self.opt(lr=self.lr), loss=glvq_loss,
                      metrics=[accuracy])
        return model

    # initialize model for prototype generation
    def _init_proto_model(self):
        return proto(ptype=self.ptype,
                     reg_rate=self.reg_rate,
                     n_poly=self.n_poly,
                     prototype_shape=self.prototype_shape,
                     env_shape=self.env_shape,
                     n_prototypes=self.n_classes,
                     init_values=self.mean_data)

    # initialize importances
    def _init_imp_model(self):
        return Imp(imptype=self.imptype,
                   shape=self.prototype_shape,
                   n_tangents=self.n_tangents,
                   n_protos=self.n_classes,
                   pca_data=self.pca_data)

    def _init_ptype(self, ptype):
        if ptype == 'const' or ptype == 'polynom' or ptype == 'neural' or ptype == 'simple_neural':
            return ptype
        else:
            raise ValueError(str(ptype) +
                             ' is no valid prototpe variant.' +
                             ' Choose const, polynom or neural')

    def _init_opt(self, opt):
        if opt is None:
            opt = RMSprop
        return opt

    def _init_imptype(self, imptype):
        if imptype == 'none' or imptype == 'relevance' or imptype == 'matrix'  or imptype == 'tangent':
            return imptype
        else:
            raise ValueError(
                str(imptype) +
                ' is no valid option as an importance. ' +
                'Choose none, relevance, matrix or tangent instead.')

    def _sort_for_classes(self, X, Y):
        X_list = list()
        for i in range(Y.shape[1]):
            X_list.append(X[np.argmax(Y, axis=-1) == i])
        return X_list

    # initialize means of data for prototype initialization
    def _init_means(self, initialize_data):
        X = initialize_data[0]
        Y = initialize_data[1]
        X_list = self._sort_for_classes(X, Y)
        means = list()
        for y_class in X_list:
            means.append(np.mean(y_class, axis=0))
        mean_data = np.vstack(means)
        return mean_data

    def _init_pca(self, initialize_data):
        X = initialize_data[0]
        Y = initialize_data[1]
        pca_list = []
        X_list = self._sort_for_classes(X, Y)
        for y_class in X_list:
            pca = PCA()
            pca.fit(y_class)
            pca_list.append(pca.components_[:, :self.n_tangents])
        pca_data = np.array(pca_list)
        return pca_data

    # Initialize Model for prediction
    def _init_prediction_model(self):
        self.prediction_layer = Softmin(self.softmin_factor)(self.distances)
        input_list = [self.input] + self.prototypes.env + \
            [self.importances.imp_input]
        prediction_model = Model(input_list, self.prediction_layer)
        prediction_model.compile(optimizer=self.opt(lr=self.lr),
                                 loss=glvq_loss,
                                 metrics=[categorical_accuracy])
        return prediction_model

    def _init_pre_train_model(self):
        self.pre_train_input = Input(shape=(self.n_classes,))
        self.regression_output = Squeezze()(
            [self.pre_train_input, self.prototypes.prototypes])
        input_list = [self.pre_train_input] + self.prototypes.env + \
            [self.importances.imp_input]
        pre_train_model = Model(input_list, self.regression_output)
        pre_train_model.compile(optimizer=self.opt(lr=self.pre_train_lr),
                                loss='mse')
        return pre_train_model

    def _pre_train(self, X, Y, epochs, pre_train_ratio, **kwargs):
        if isinstance(X, list) and self.ptype == 'const':
            n_pre = int(X[0].shape[0] * pre_train_ratio)
            self.pre_train_model.fit(Y[:n_pre], X[0][:n_pre],
                                     epochs=epochs, **kwargs)
        elif isinstance(X, list) and self.ptype != 'const':
            n_pre = int(X[0].shape[0] * pre_train_ratio)
            self.pre_train_model.fit([Y[:n_pre], X[1][:n_pre]], X[0][:n_pre],
                                     epochs=epochs, **kwargs)
        else:
            n_pre = int(X.shape[0] * pre_train_ratio)
            self.pre_train_model.fit(Y[:n_pre], X[:n_pre], epochs=epochs)
        return n_pre

    def _init_aux_loss_model(self):
        self.aux_input = Input(shape=(self.n_classes,))
        self.aux_output = Squeezze(name='prototype_output')(
            [self.aux_input, self.prototypes.prototypes])
        input_list = [self.input] + [self.aux_input] + self.prototypes.env + \
            [self.importances.imp_input]
        model = Model(input_list, [self.distances, self.aux_output])
        model.compile(optimizer=self.opt(lr=self.lr),
                      loss={'prototype_output': 'mse',
                            'distance': glvq_loss},
                      loss_weights={'prototype_output': self.aux_factor,
                                    'distance': self.distance_factor},
                      metrics={'prototype_output': 'acc',
                               'distance': [accuracy]})
        return model

    def generate_proto(self, env):
        protos = self.prototypes.generate_proto(env)
        proto_list = list()
        for i in range(protos.shape[1]):
            proto_list.append(protos[:, i, :])
        return proto_list

    def fit(self, X, Y,
            epochs=100,
            epochs_pre_train=50,
            pre_train_ratio=0.25,
            **kwargs):
        """
        Train model on data X, y

        Parameters
        ----------
        X : TYPE
            Training input data.
        Y : TYPE
            Correct labels.
        epochs : int, optional
            Epochs. The default is 100.
        epochs_pre_train : int, optional
            Epochs of pretraining. The default is 50.

        Returns
        -------
        None.

        """
        n_pre = 0
        if self.enable_pre_train:
            n_pre = self._pre_train(X, Y, epochs=epochs_pre_train,
                                    pre_train_ratio=pre_train_ratio,
                                    **kwargs)
        if isinstance(X, list) and self.ptype == 'const':
            if self.aux_factor == 0:
                self.model.fit(X[0][n_pre:], Y[n_pre:],
                               epochs=epochs, **kwargs)
            else:
                self.aux_model.fit([X[0][n_pre:], Y[n_pre:]],
                                   {'prototype_output': X[0][n_pre:],
                                    'distance': Y[0][n_pre:]}, epochs=epochs,
                                   **kwargs)
        else:
            if self.aux_factor == 0:
                if isinstance(X, list):
                    self.model.fit([x[n_pre:] for x in X],
                                   Y[n_pre:], epochs=epochs, **kwargs)
                else:
                    self.model.fit(X[n_pre:],
                                   Y[n_pre:], epochs=epochs, **kwargs)
            else:
                self.aux_model.fit([X[0][n_pre:], Y[n_pre:], X[1][n_pre:]],
                                   {'prototype_output': X[0][n_pre:],
                                    'distance': Y[n_pre:]},
                                   epochs=epochs, **kwargs)

    def score(self, X, Y, **kwargs):
        """
        score function

        Parameters
        ----------
        X : TYPE
            Data to classify.
        Y : TYPE
            Correct labels as one-hot-encoding.

        Returns
        -------
        loss float
            DESCRIPTION.
        accuracy float

        """
        if isinstance(X, list) and self.ptype == 'const':
            return self.prediction_model.evaluate(X[0], Y, **kwargs)
        else:
            return self.prediction_model.evaluate(X, Y, **kwargs)

    def predict(self, X, **kwargs):
        if isinstance(X, list) and self.ptype == 'const':
            return self.prediction_model.predict(X[0], **kwargs)
        else:
            return self.prediction_model.predict(X, **kwargs)

    def get_distances(self, X, **kwargs):
        return self.model.predict(X, **kwargs)

    def get_importances(self):
        if self.imptype == 'none':
            raise Exception('No importances for this imptype')
        else:
            if self.aux_factor > 0:
                weights = self.model.get_layer('importance').get_weights()[0]
            else:
                weights = self.model.get_layer('importance').get_weights()[0]
        return weights

    def plot_model(self, file, **kwargs):
        plot_model(model=self.model,
                   to_file='figures\\' + file,
                   show_shapes=True,
                   **kwargs)

    def plot_prototypes_2d(self, env=None, multi=True, **kwargs):
        """
        Plot Prototypes in a 2d figure

        Parameters
        ----------
        env : TYPE, optional
            Environmental data, if generative prototype path is used.
            The default is None.
        multi : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        if self.ptype != 'const':
            ara = plotting.create_ara(env)
            proto_list = self.generate_proto(ara)
            if multi:
                plotting.plot_multi_prototypes_2d_over_env(proto_list, ara=ara,
                                                           **kwargs)
            else:
                for p_num, prototype in enumerate(proto_list):
                    plotting.plot_prototypes_over_env_2d(prototype, ara=ara,
                                                         p_number=p_num,
                                                         **kwargs)
        else:
            protos = self.model.get_layer('prototypes_constant').get_weights()[0]
            plotting.plot_constant_prototypes(protos, **kwargs)

    def plot_prototypes_3d(self, fname, multi=False, env=None, **kwargs):
        if self.ptype == 'const':
            raise Exception('3D Plot not available for constant prototypes')
        else:
            ara = plotting.create_ara(env)
            proto_list = self.generate_proto(ara)
            if multi:
                plotting.plot_multi_prototypes_3d_over_env(
                    ara,
                    proto_list,
                    fname,
                    **kwargs)
            else:
                for index, prototype in enumerate(proto_list):
                    plotting.plot_prototypes_over_env_3d(
                        prototype,
                        ara,
                        fname=fname + '_' + str(index),
                        **kwargs)

    def plot_training_curves(self, pre_train=False,
                             name='Model Loss over Epochs'):
        """
        Plot loss and accuracy over epochs

        Parameters
        -------
        pre_train : Bool
            Plot pretraining curves or normal training

        Returns
        -------
        None.

        """
        if pre_train:
            name = 'Model Loss over Epochs (Pretraining)'
            plotting.plot_training_curves(self.pre_train_model, name=name)
        else:
            name = 'Model Loss over Epochs (Training)'
            if self.aux_factor > 0:
                plotting.plot_training_curves(self.aux_model, name=name)
            else:
                plotting.plot_training_curves(self.model, name=name)

    def plot_distance_histogram(self, X, Y, bins=20,
                                name='Projected Distance Histogram',
                                **kwargs):
        """
        Create distance histogram plot

        Parameters
        ----------
        X : TYPE
            DESCRIPTION.
        Y : TYPE
            DESCRIPTION.
        bins : TYPE, optional
            DESCRIPTION. The default is 20.
        name : TYPE, optional
            DESCRIPTION. The default is 'Projected Distance Histogram'.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if isinstance(X, list) and self.ptype == 'const':
            distances = self.model.predict(X[0], **kwargs)
        else:
            distances = self.model.predict(X, **kwargs)
        plotting.dist_hist(distances, Y, bins, name)

    def plot_importances(self):
        """
        Plot the importance vector/matrices

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # if self.imptype == 'none':
        #     raise Exception('No importances to plot')

        # else:
        #     if self.aux_factor > 0:
        #         weights = self.model.get_layer('importance').get_weights()[0]
        #     else:
        #         weights = self.model.get_layer('importance').get_weights()[0]
        weights = self.get_importances()
        if self.imptype == 'matrix':
            plotting.plot_importances(weights)
        elif self.imptype == 'tangent':
            for i in range(self.n_classes):
                plotting.plot_importances(weights[i, :, :])
        else:
            plotting.plot_importances(weights)

    def plot_prediction(self, X, Y, **kwargs):
        prediction = self.predict(X, **kwargs)
        if len(X) > 1:
            C = X[1]
        plotting.plot_prediction(Y, prediction, C=X[1])

    def plot_feature_values(self, env, data=None, steps=20, **kwargs):
        """
        Plot features of different classes over context factor.

        Parameters
        ----------
        env : TYPE
            Context factor.
        data : list, optional
            Dataset List of samples and according labels. The default is None.
        steps : TYPE, optional
            DESCRIPTION. The default is 20.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if self.ptype == 'const':
            print('Feature plot over environment factor not possible for constant prototypes')
        else:
            if data is not None:
                # Inititalization
                means = list()
                std = list()

                # Data
                x = data[0]
                env = np.squeeze(env)

                # Label preperation
                if len(data[1].shape) > 1:
                    y = np.argmax(data[1], axis=-1)
                else:
                    y = data[1]

                # Create context buckets
                c_min = np.min(env)
                c_max = np.max(env)
                buckets = np.arange(c_min, c_max, (c_max-c_min)/steps)

                # Find samples in buckets
                bucket_idx_list = [
                    ((env >= min_limit) & (env <= max_limit))
                    for min_limit, max_limit in zip(buckets[:-1], buckets[1:])]

                x_bucket = [x[bucket_idx] for bucket_idx in bucket_idx_list]
                y_bucket = [y[bucket_idx] for bucket_idx in bucket_idx_list]

                # Statistics
                for i in range(self.n_classes):
                    x_buckets_per_class_list = [
                        x_bucket[bucket_idx][y_bucket[bucket_idx] == i]
                        for bucket_idx in range(len(x_bucket))]
                    means.append([
                        np.mean(x_buckets_per_class, axis=0)
                        for x_buckets_per_class in x_buckets_per_class_list])
                    std.append([
                        np.std(x_buckets_per_class, axis=0)
                        for x_buckets_per_class in x_buckets_per_class_list])

                # Prototypes
                env_protos = [bucket-(bucket - bucket_old)/2 for bucket, bucket_old in zip(buckets[1:], buckets[:-1])]
                prototypes = self.generate_proto(env_protos)

                # Plot
                plotting.plot_features_over_env(means, std, env_protos,
                                                prototypes, **kwargs)

            else:
                ara = plotting.create_ara(env, steps=steps)
                protos = self.generate_proto(ara)
                for i_proto in protos:
                    features = list()
                    for i in range(i_proto.shape[1]):
                        features.append(i_proto[:, i])
                    plotting.plot_features_over_env_proto(features, ara)

    def plot_accuracy_over_env(self, X, Y, steps=20, **kwargs):
        # Label preperation
        if len(Y.shape) > 1:
            Y = np.argmax(Y, axis=-1)

        # Create context buckets
        env = np.squeeze(X[1])
        c_min = np.min(env)
        c_max = np.max(env)
        buckets = np.arange(c_min, c_max, (c_max-c_min)/steps)

        # Find samples in buckets
        bucket_idx_list = [
            ((env >= min_limit) & (env <= max_limit))
            for min_limit, max_limit in zip(buckets[:-1], buckets[1:])]

        # Predict
        predictions = self.predict(X, **kwargs)
        predictions = np.argmax(predictions, axis=-1)

        # Sort to buckets
        predictions_bucket = [predictions[bucket_idx]
                              for bucket_idx in bucket_idx_list]
        Y_bucket_list = [Y[bucket_idx] for bucket_idx in bucket_idx_list]

        # Calculate accuracy
        bucket_accuracy = [sum(Y_bucket == prediction)/len(prediction)
                           for Y_bucket, prediction
                           in zip(Y_bucket_list, predictions_bucket)]

        # Plot
        plotting.plot_acc_over_env(bucket_accuracy, buckets)

    def plot_confusion(self, X, Y, **kwargs):
        prediction = self.predict(X, **kwargs)
        prediction = np.argmax(prediction, axis=-1)
        plotting.plot_confusion(Y, prediction)

    def save_model(self, filename='model'):
        """
        Save model to hard drive

        Parameters
        ----------
        filename : TYPE, optional
            DESCRIPTION. The default is 'model'.

        Returns
        -------
        None.

        """
        model_dir = os.path.dirname(__file__)

        if self.aux_factor > 0:
            self.aux_model.save(model_dir + '/models/' + filename + '.h5')
        else:
            self.model.save(model_dir + '/models/' + filename + '.h5')
        config_data = {
            'n_classes': self.n_classes,
            'ptype': self.ptype,
            'imptype': self.imptype,
            # 'opt': self.opt,
            'learning_rate': self.lr,
            'pre_train_lr': self.pre_train_lr,
            'prototype_shape': self.prototype_shape,
            'env_shape': self.env_shape,
            'reg_rate': self.reg_rate,
            'n_poly': self.n_poly,
            'aux_factor': self.aux_factor,
            'pre_training': self.enable_pre_train,
            'n_tangents': self.n_tangents,
            'softmin_factor': self.softmin_factor}

        with open(model_dir + '/models/' + filename + '.json', 'w') as outfile:
            json.dump(config_data, outfile)

    def load_model_weights(self, filename):
        return self.model.load_weights(filename)

    def compile_model(self):
        self._compile_model(self.model)


def load(filename='model'):
    """
    Load a saved model. Model is automatically initialised and compiled.

    Parameters
    ----------
    filename : string, optional
        DESCRIPTION. The default is 'model'.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    model : alvg_model
        Compiled model. Ready to be trained or evaluated.

    """
    model_dir = os.path.dirname(__file__)
    with open(model_dir + '/models/' + filename + '.json') as json_file:
        config_data = json.load(json_file),
        config_data = config_data[0]
        model = Alvq_Model(
            n_classes=config_data['n_classes'],
            ptype=config_data['ptype'],
            imptype=config_data['imptype'],
            # opt=config_data['opt'],
            learning_rate=config_data['learning_rate'],
            pre_train_lr=config_data['pre_train_lr'],
            prototype_shape=tuple(config_data['prototype_shape']),
            env_shape=tuple(config_data['env_shape']),
            reg_rate=config_data['reg_rate'],
            n_poly=config_data['n_poly'],
            aux_factor=config_data['aux_factor'],
            pre_training=config_data['pre_training'],
            n_tangents=config_data['n_tangents'],
            softmin_factor=config_data['softmin_factor'])
    model.load_model_weights(model_dir + '/models/' + filename + '.h5')
    model.compile_model()
    return model
