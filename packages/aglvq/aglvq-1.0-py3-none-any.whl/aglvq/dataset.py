"""
Implementation of artificial dataset
"""
import numpy as np
from sklearn.model_selection import train_test_split
from . import plotting


def create_dataset(set_type='const', split=True, num_samples=3000,
                   x_start=0, x_stop=4*np.pi, height_tri=10,
                   n_fft=64, n_classes=3, amp_noise=0.5):
    """
    Creates sythetic dataset

    Parameters
    ----------
    set_type : string, optional
        Possible options are:
            'const': Constant classes with noise
            'variable': Variable samples with linear c-factor
            'nonLinear': Variable samples with non linear c-factor.
            The default is 'const'.
    split : TYPE, optional
        DESCRIPTION. The default is True.
    num_samples : int, optional
        Number of samples. The default is 3000.
    x_start : TYPE, optional
        DESCRIPTION. The default is 0.
    x_stop : TYPE, optional
        DESCRIPTION. The default is 2*np.pi.
    height_tri : float, optional
        Height of the triangle. The default is 10.
    n_fft : int, optional
        Number of features of each sample. The default is 64.
    n_classes : int, optional
        Number of classes. The default is 3.
    amp_noise : float, optional
        Amplitude of added noise. The default is 0.5.

    Returns
    -------
    dataset : list
        [X_train, Y_train, C_train, X_test, Y_test, C_test].

    """
    n_c = num_samples//n_classes
    num = int(n_fft/2)

    y1 = list()
    y2 = list()
    y3 = list()
    labels = list()
    x = np.arange(start=x_start, stop=x_stop, step=x_stop/n_c)
    if set_type == 'const':
        c = np.ones(n_c)
        c_return = c
    if set_type == 'variable':
        c = np.arange(start=x_start, stop=x_stop, step=x_stop/n_c)
        c_return = c
    elif set_type == 'nonLinear':
        c = np.cos(x)
        c_return = x
    for i in range(n_c):
        noise = np.random.uniform(-amp_noise,
                                  amp_noise, size=(n_classes, n_fft))
        y11 = [1*c[i] * x + noise[0, k] for k, x in
               enumerate(np.linspace(start=0, stop=height_tri, num=num))]
        y12 = [(-1*c[i])*x + noise[0, k] for k, x in
               enumerate(np.linspace(start=0, stop=height_tri, num=num))]
        y12 = [value + y11[-1] for value in y12]
        y1.append(np.concatenate((y11, y12)))

        y2.append(np.ones((n_fft,)) * 5 * c[i] + 5 + noise[1, :])
        y3.append(np.cos(np.linspace(start=0, stop=n_fft, num=n_fft))
                  * 5 * c[i] + noise[2, :])

    y1 = np.array(y1)+10
    y2 = np.array(y2)
    y3 = np.array(y3)
    labels = np.concatenate((np.zeros(n_c, ), np.ones((n_c, )),
                             np.ones((n_c, ))*2))
    y_values = np.concatenate((y1, y2, y3))

    dataset = list()
    dataset.append(y_values)
    dataset.append(labels)
    dataset.append(np.concatenate((c_return, c_return, c_return)))
    if split:
        dataset = split_shuffle(dataset)
    return dataset


def split_shuffle(dataset):
    combined_array = np.concatenate(
        (dataset[0],
         np.expand_dims(dataset[1], axis=-1),
         np.expand_dims(dataset[2], axis=-1)), axis=-1)
    split_array = train_test_split(combined_array, shuffle=True,
                                   random_state=111, test_size=0.3)
    data_list = list()
    for array in split_array:
        data_list.append(array[:, :-2])
        data_list.append(array[:, -2])
        data_list.append(array[:, -1])
    return data_list
