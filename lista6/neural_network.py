import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def error(y1, y2):
    a = 0
    for i in range(len(y1)):
        a += (y1[i] - y2[i]) ** 2
    return a[0]


def sigmoid_derivative(x):
    return x * (1.0 - x)


def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return 1. * (x > 0)


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return 1.0 - np.tanh(x) ** 2


class NeuralNetwork:
    def __init__(self, x, y, layer1='sigmoid', layer2='relu', layer_size=4,
                 eta=0.05, xor=False):
        self.l1 = layer1
        self.l2 = layer2
        self.input = x
        self.eta = eta
        if xor:
            if layer1 == "relu":
                np.random.seed(17)
            else:
                np.random.seed(3)
        self.weights1 = np.random.rand(
            layer_size, int(self.input.size / self.input.shape[0]))
        if xor:
            if layer1 == "relu":
                np.random.seed(17)
            else:
                np.random.seed(3)
        self.weights2 = np.random.rand(1, layer_size)
        self.y = y
        self.y.shape = [self.y.shape[0], 1]

        self.output = np.zeros([self.y.shape[0], 1])

    def feed_forward(self):
        if self.l1 == 'sigmoid':
            self.layer1 = sigmoid(np.dot(self.input, self.weights1.T))
        elif self.l1 == 'tanh':
            self.layer1 = tanh(np.dot(self.input, self.weights1.T))
        else:
            self.layer1 = relu(np.dot(self.input, self.weights1.T))

        if self.l2 == 'sigmoid':
            self.output = sigmoid(np.dot(self.layer1, self.weights2.T))
        elif self.l1 == 'tanh':
            self.output = tanh(np.dot(self.layer1, self.weights2.T))
        else:
            z = np.dot(self.layer1, self.weights2.T)
            self.output = relu(z)

    def back_prop(self):
        if self.l2 == 'sigmoid':
            delta2 = (self.y - self.output) * sigmoid_derivative(self.output)
        elif self.l2 == 'tanh':
            delta2 = (self.y - self.output) * tanh_derivative(self.output)
        else:
            delta2 = (self.y - self.output) * relu(self.output)

        d_weights2 = self.eta * np.dot(delta2.T, self.layer1)

        if self.l1 == 'sigmoid':
            delta1 = sigmoid_derivative(self.layer1) * np.dot(delta2,
                                                              self.weights2)
        elif self.l1 == 'tanh':
            delta1 = tanh_derivative(self.layer1) * np.dot(delta2,
                                                           self.weights2)
        else:
            delta1 = relu_derivative(self.layer1) * np.dot(delta2,
                                                           self.weights2)
        d_weights1 = self.eta * np.dot(delta1.T, self.input)

        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def predict(self, input):
        if self.l1 == 'sigmoid':
            l1 = sigmoid(np.dot(input, self.weights1.T))
        elif self.l1 == 'tanh':
            l1 = tanh(np.dot(input, self.weights1.T))
        else:
            l1 = relu(np.dot(input, self.weights1.T))

        if self.l2 == 'sigmoid':
            return sigmoid(np.dot(l1, self.weights2.T))
        elif self.l1 == 'tanh':
            return tanh(np.dot(l1, self.weights2.T))
        else:
            return relu(np.dot(l1, self.weights2.T))
