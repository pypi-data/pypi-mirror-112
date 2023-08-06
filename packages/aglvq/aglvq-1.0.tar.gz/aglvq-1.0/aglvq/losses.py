"""Implementations of losses.
"""
import keras.backend as K


class GlvqLossOverDissimilarities(object):
    def __call__(self, y_true, y_pred):
        dp = K.sum(y_true * y_pred, axis=-1)

        dm = K.min((1 - y_true) * y_pred + y_true * 1 / K.epsilon(),
                   axis=-1)

        loss = (dp - dm) / (dp + dm)

        return loss


def glvq_diss_loss(y_true, y_pred):
    loss_func = GlvqLossOverDissimilarities()
    return loss_func(y_true, y_pred)


def glvq_sigmoid_loss(y_true, y_pred):
    mu_func = GlvqLossOverDissimilarities()
    mu = mu_func(y_true, y_pred)
    f = 1 / (1 + K.exp(-mu))
    return f


def glvq_swish_loss(y_true, y_pred):
    mu_func = GlvqLossOverDissimilarities()
    mu = mu_func(y_true, y_pred)
    loss = mu * 1 / (1+K.exp(-mu))

    return loss
