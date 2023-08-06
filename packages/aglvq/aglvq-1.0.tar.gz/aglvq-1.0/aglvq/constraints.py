"""Implementations of constraint functions for the weights of the importances.
"""
from keras import backend as K
from keras.constraints import Constraint


def mixed_shape(inputs):
    if not K.is_tensor(inputs):
        raise ValueError('Input must be a tensor.')
    else:
        with K.name_scope('mixed_shape'):
            int_shape = list(K.int_shape(inputs))
            # sometimes int_shape returns mixed integer types
            int_shape = [int(i) if i is not None else i for i in int_shape]
            tensor_shape = K.shape(inputs)

            for i, s in enumerate(int_shape):
                if s is None:
                    int_shape[i] = tensor_shape[i]
            return tuple(int_shape)


def svd(tensors, full_matrices=False, compute_uv=True):
    if K.backend() == 'tensorflow':
        import tensorflow as tf
        # return s, u, v
        return tf.compat.v1.svd(tensors, full_matrices=full_matrices,
                                compute_uv=compute_uv)

    else:
        raise NotImplementedError("Unknown backend `" + K.backend() + "`.")


def orthogonalization(tensors):
    out = []
    for i in range(tensors.shape[0]):
        # orthogonalization via polar decomposition
        _, u, v = svd(tensors[i, :, :], full_matrices=False, compute_uv=True)
        u_shape = mixed_shape(u)
        v_shape = mixed_shape(v)

        # reshape to (num x N x M)
        u = K.reshape(u, (-1, u_shape[-2], u_shape[-1]))
        v = K.reshape(v, (-1, v_shape[-2], v_shape[-1]))

        out_element = K.batch_dot(u, K.permute_dimensions(v, [0, 2, 1]))

        out.append(K.reshape(out_element, u_shape[:-1] + (v_shape[-2],)))

    out_tensor = out[0]
    out_tensor = K.expand_dims(out_tensor, axis=0)
    out_tensor = K.concatenate((out_tensor, out[1:]), axis=0)
    return out_tensor


class Orthogonalization(Constraint):
    def __call__(self, w):
        return orthogonalization(w)


class Normalization(Constraint):
    def __call__(self, w):
        delta_mat = K.dot(w, K.transpose(w))
        trace_delta = K.sum(K.eye(K.shape(w)[0])*delta_mat, axis=-1)
        sum_trace = K.sum(trace_delta, axis=-1)
        factor = K.sqrt(sum_trace)

        return w/factor


class Relevance_Normalization(Constraint):
    def __call__(self, w):
        factor = K.sum(w)

        return w/factor
