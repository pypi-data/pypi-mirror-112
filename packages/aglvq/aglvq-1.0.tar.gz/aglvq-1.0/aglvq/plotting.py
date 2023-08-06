import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import pandas as pd
from sklearn.metrics import confusion_matrix
from .confusion_matrix import pretty_plot_confusion_matrix

def create_ara(c, steps=10):
    mini = np.min(c)
    maxi = np.max(c)
    if (maxi-mini) > 0:
        ara = np.arange(start=mini, stop=maxi, step=(maxi-mini)/steps)
    else:
        ara = np.ones(steps)
    return ara


def plot_constant_prototypes(prototypes,
                             directory='figures\\',
                             title='',
                             xlabel='Features [-]',
                             ylabel='Value [-]',
                             size=[6.2992, 2],
                             fname='constant_prototypes',
                             save=False,
                             single_figures=False):
    colo = matplotlib.cm.YlOrBr(255)
    if single_figures:
        for proto in prototypes:
            plt.figure(figsize=size, tight_layout=True)
            plt.plot(proto, c=colo)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
        if save:
            plt.savefig(directory + fname + '.png', dpi=500)
    else:
        plt.figure(figsize=size, tight_layout=True)
        marker = ['-', '--', ':', '-.']
        for i, proto in enumerate(prototypes):
            plt.plot(proto, linestyle=marker[i], c=colo)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
        if save:
            plt.savefig(directory + fname + '.png', dpi=500)


def plot_prototypes_over_env_2d(
        signal,
        ara,
        fname,
        xlabel='Features [-]',
        ylabel='$v [m/s]$',
        zlabel='Value [-]',
        title='Prototypen nach Geschwindigkeit sortiert',
        directory='figures\\',
        size=[6.2992, 2],
        save=False):
    """
    Plot single Signal/Prototype per class
    """
    plt.figure(tight_layout=True, figsize=size)
    cm = matplotlib.cm
    colormaps = [cm.YlOrBr, cm.Reds, cm.Greens]
    c_offset = 30
    index_c = np.arange(start=c_offset, stop=255 + (255-c_offset)//len(signal),
                        step=(255-c_offset)//len(signal))
    c = [colormaps[0](i) for i in index_c]
    for i in range(len(signal)):
        plt.plot(signal[i], color=c[i+1],  # color=c2+i/10*d_c,
                 label='v = ' + str(int(ara[i]))+'km/h')

    plt.ylabel(ylabel, fontsize=11)
    plt.xlabel(xlabel, fontsize=11)
    if save:
        plt.savefig(directory + fname + '_protos_vis_2d' + '.png', dpi=1200)


def plot_multi_prototypes_2d_over_env(
        signal_list,
        ara,
        fname,
        xlabel='$Features [-]$',
        ylabel='$Value [-]$',
        title='Prototypen nach Geschwindigkeit sortiert',
        directory='figures\\',
        size=[6.2992, 2],
        save=False):
    """
    Plot multiple Signals/Prototypes per class
    """

    plt.figure(figsize=size, tight_layout=True)
    cm = matplotlib.cm
    colormaps = [cm.Blues, cm.Reds, cm.Greens]
    c_offset = 50

    for j, signal in enumerate(signal_list):
        # d_c = c[j] - c2[j]
        index_c = np.arange(start=c_offset,
                            stop=255 + (255-c_offset)//len(signal),
                            step=(255-c_offset)//len(signal))
        c = [colormaps[j](i) for i in index_c]
        for i in range(len(signal)-1):
            plt.plot(signal[i], color=c[i+1])
        i = i + 1
        plt.plot(signal[i], color=c[i+1],
                 label='class' + str(j))
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if save:
        plt.savefig(directory + fname + '_protos_vis_2d_multi' + '.png',
                    dpi=1200)


def plot_prototypes_over_env_3d(
        signal,
        ara,
        fname,
        xlabel='Features [-]',
        ylabel='$v [m/s]$',
        zlabel='Value [-]',
        title='Prototypen nach Geschwindigkeit sortiert',
        directory='figures\\',
        size=[20, 10],
        save=False):
    """
    Plot multiple Signals/Prototypes per class in 3d
    """
    plt.figure(figsize=size, constrained_layout=True)
    ax = plt.axes(projection='3d')
    length = signal.shape[1]
    x, y = np.meshgrid(np.arange(length), ara)

    ax.plot_surface(x, y, signal, cmap='viridis')
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel(zlabel, rotation=90)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    if save:
        plt.savefig(directory + fname + '_3d' + '.png', dpi=500)


def plot_multi_prototypes_3d_over_env(
        c,
        signal_list,
        fname,
        xlabel='Features [-]',
        ylabel='$c [-]$',
        zlabel='Value [-]',
        title='',
        directory='figures\\',
        size=[20, 10],
        save=False):
    ara = create_ara(c, steps=c.shape[0])

    plt.figure(figsize=size, constrained_layout=True)
    ax = plt.axes(projection='3d')
    length = signal_list[0].shape[1]
    x, y = np.meshgrid(np.arange(length), ara)

    for index, signal in enumerate(signal_list):
        ax.plot_surface(x, y, signal)
    ax.set_zlabel(zlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_title(title)
    if save:
        plt.savefig('figures/' + fname + '_3d_multi' + '.pdf', dpi=1200)


def plot_example_protos(protos,
                        x_signals,
                        y_signals,
                        labels):
    """
    Plots 3 example signals and the prototype of every class
    """
    colo = ['m', 'c', 'r']

    fig, ax = plt.subplots(3)
    for i in range(3):
        for j, proto in enumerate(protos):
            ax[i].plot(proto[i], c=colo[j],
                       label='Prototypen_' + labels[j])
        ax[i].plot(x_signals[i, :], '--', label='signal')
        s = np.argmax(y_signals[i])
        ax[i].set_title('Prototyenverteilung, Klasse ' + labels[s])
        ax[i].legend()


def dist_hist(distances,
              y_signals,
              bins=20,
              name='Projected Distance Histogram'):
    """
    Plot histogram for distances
    """
    dist_true = distances*y_signals
    dist_true = dist_true[dist_true != 0]
    dist_true = dist_true[dist_true != 0]
    dist_false = distances * (np.ones(distances.shape) - y_signals)
    dist_false = dist_false[dist_false != 0]
    dist_hist_true = np.histogram(dist_true, bins=bins)
    dist_hist_false = np.histogram(dist_false, bins=bins)

    plt.figure()
    plt.plot(dist_hist_false[1][:-1],
             dist_hist_false[0],
             label='false',
             color='r')
    plt.plot(dist_hist_true[1][:-1],
             dist_hist_true[0],
             label='true',
             color='g')
    plt.legend()
    plt.title(name)
    plt.xlabel('Projected Distance')
    plt.ylabel('Number of Samples [-]')
    plt.grid()


def plot_training_curves(model, name='Model Loss over Epochs'):
    """
    Plot Training curves for training of a classifier

    Parameters
    ----------
    model : Keras model

    Returns
    -------
    None.

    """
    plt.figure()
    plt.plot(model.history.history['loss'], label='loss')
    keys = list(model.history.history.keys())
    if 'accuracy' in keys:
        plt.plot(model.history.history['accuracy'], label='accuracy')
        plt.ylim(top=1.5)
    if 'distance_accuracy' in keys:
        plt.plot(model.history.history['distance_accuracy'], label='accuracy')
        plt.ylim(top=1.5)
    if 'lr' in keys:
        plt.plot(model.history.history['lr'], label='learning rate')
    plt.legend()
    plt.title(name)
    plt.ylabel('Loss [-]')
    plt.xlabel('Epochs [-]')
    plt.grid()


def plot_importances(importances):
    fig = plt.figure(tight_layout=True)
    if len(importances.shape) == 1:
        mat = np.eye(importances.shape[0]) * importances
    else:
        mat = importances
    im = plt.imshow(mat)
    fig.colorbar(im)
    plt.title('Projection Matrix')


def plot_features_over_env_proto(features,
                                 env,
                                 ylabel='Value',
                                 xlabel='Env Value'):
    plt.figure(tight_layout=True)
    for index, feature in enumerate(features):
        plt.plot(env, feature)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)


def plot_features_over_env(mean_features,
                           std_features,
                           env,
                           prototypes,
                           ylabel='Value',
                           xlabel='Env Value',
                           n_features=None,
                           size=[10, 7],
                           save=False):
    if n_features is not None:
        if isinstance(n_features, int):
            numerator = range(n_features)
        elif isinstance(n_features, list):
            numerator = n_features
            n_features = len(n_features)
        else:
            raise ValueError('You need to provide an integer with the number of features or a list with the indices of the features')
    else:
        n_features = len(mean_features[0][0])
        numerator = range(n_features)

    cm = matplotlib.cm.viridis
    n_classes = len(mean_features)
    color_index = np.arange(start=0, stop=255, step=255//n_classes)
    fig, ax = plt.subplots(n_features, tight_layout=True, figsize=size)
    if n_features == 1:
        ax = [ax]
    for idx_class in range(n_classes):
        for plot_index, index in enumerate(numerator):
            c = cm(color_index[idx_class])
            c_fill = list(c)
            c_fill[-1] = 0.2
            c_fill = tuple(c_fill)
            mean_feature = np.array(
                [value[index] for value in mean_features[idx_class]])
            std_feature = np.array(
                [value[index] for value in std_features[idx_class]])
            ax[plot_index].plot(env, mean_feature, label='Mean', c=c)
            ax[plot_index].fill_between(env,
                                        mean_feature + std_feature,
                                        mean_feature - std_feature,
                                        color=c_fill)
            ax[plot_index].plot(env,
                                prototypes[idx_class][:, index],
                                '--', label='Prototype', c=c)
            ax[plot_index].set_xlabel(xlabel, fontsize=11)
            ax[plot_index].set_ylabel(ylabel, fontsize=11)
    if save:
        plt.savefig('figures/' + 'features' + '.png', dpi=2000)


def plot_acc_over_env(acc,
                      env,
                      ylabel='Accuracy [-]',
                      xlabel='Env Value [-]',
                      save=False):
    plt.figure(tight_layout=True)
    plt.plot(env[:-1], acc)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)


def plot_prediction(Y, prediction, C=None):
    plt.figure()
    ax = plt.subplot(Y.shape[1]+1, 1, 1)
    for i in range(Y.shape[1]):
        plt.subplot(Y.shape[1]+1, 1, i+1, sharex=ax)
        plt.plot(prediction[:, i],
                 color=[0.8, 0.15, 0.15],
                 label='Prediction Class {}'.format(i))
        plt.plot(Y[:, i], color='black', label='Label')
        plt.ylabel('Prediction')
        plt.grid()
        plt.legend()
    plt.xlabel('samples')
    plt.subplot(Y.shape[1]+1, 1, i+2, sharex=ax)
    if C is not(None):
        plt.plot(C)
        plt.ylabel('Environment')
    plt.grid()


def plot_confusion(Y, prediction):
    conf = confusion_matrix(np.argmax(Y, axis=1), prediction)
    pretty_plot_confusion_matrix(pd.DataFrame(conf), figsize=None)
    plt.ylim([Y.shape[1]+1, 0])
