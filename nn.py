import math

import numpy as np


class NeuralNetwork:
    def __init__(self, x):
        self.input = np.asarray([x])
        self.weights = []
        self.weights.append(np.random.rand(self.input.shape[1], 16))
        self.weights.append(np.random.rand(16, 8))
        self.weights.append(np.random.rand(8, 1))

    def feedforward(self):
        layer = self.input
        for weight in self.weights:
            dot_product = np.dot(layer, weight)
            layer = relu_v(dot_product)
        return layer


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def relu(x):
    if x < 0:
        return 0
    elif x >= 0:
        return x


sigmoid_v = np.vectorize(sigmoid)
relu_v = np.vectorize(relu)
