from keras.initializers import Initializer


class Mean_Initializer(Initializer):
    def __init__(self, mean_spektrums):
        self.mean_spektrums = mean_spektrums

    def __call__(self, shape, dtype=None):
        return self.mean_spektrums


class PCA_Initializer(Initializer):
    def __init__(self, pca_data):
        self.pca_data = pca_data

    def __call__(self, shape, dtype=None):
        return self.pca_data
