import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return 1.0 - np.tanh(x) ** 2


def error(y1, y2):
    a = 0
    for i in range(len(y1)):
        a += (y1[i] - y2[i]) ** 2
    return a[0]


class NeuralNetwork:
    def __init__(self, x, y, sygmoid=True):
        self.input = x
        self.eta = 0.5
        self.weights1 = np.random.rand(10, int(
            self.input.size / self.input.shape[0]))
        self.weights2 = np.random.rand(10, 10)
        self.weights3 = np.random.rand(1, 10)
        self.y = y
        self.y.shape = [self.y.shape[0], 1]
        self.output = np.zeros(self.y.shape)
        self.layer1 = np.zeros(10)
        self.layer2 = np.zeros(10)
        self.sygmoid = sygmoid

    def feed_forward(self):
        if self.sygmoid:
            self.layer1 = sigmoid(np.dot(self.input, self.weights1.T))
            self.layer2 = sigmoid(np.dot(self.layer1, self.weights2.T))
            self.output = sigmoid(np.dot(self.layer2, self.weights3.T))
        else:
            self.layer1 = tanh(np.dot(self.input, self.weights1.T))
            self.layer2 = tanh(np.dot(self.layer1, self.weights2.T))
            self.output = tanh(np.dot(self.layer2, self.weights3.T))

    def back_prop(self):
        if self.sygmoid:

            delta3 = (self.y - self.output) * sigmoid_derivative(self.output)
            d_weights3 = sigmoid_derivative(self.eta) * np.dot(delta3.T,
                                                               self.layer2)
            delta2 = sigmoid_derivative(self.layer2) * np.dot(delta3,
                                                              self.weights3)
            d_weights2 = sigmoid_derivative(self.eta) * np.dot(delta2.T,
                                                               self.layer1)
            delta1 = sigmoid_derivative(self.layer1) * np.dot(delta2,
                                                              self.weights2)
            d_weights1 = sigmoid_derivative(self.eta) * np.dot(delta1.T,
                                                               self.input)
        else:
            delta3 = (self.y - self.output) * tanh_derivative(self.output)
            d_weights3 = tanh_derivative(self.eta) * np.dot(delta3.T,
                                                            self.layer2)
            delta2 = tanh_derivative(self.layer2) * np.dot(delta3,
                                                           self.weights3)
            d_weights2 = tanh_derivative(self.eta) * np.dot(delta2.T,
                                                            self.layer1)
            delta1 = tanh_derivative(self.layer1) * np.dot(delta2,
                                                           self.weights2)
            d_weights1 = tanh_derivative(self.eta) * np.dot(delta1.T,
                                                            self.input)

        self.weights1 += d_weights1
        self.weights2 += d_weights2
        self.weights3 += d_weights3

    def predict(self, input):
        if self.sygmoid:
            self.layer1 = sigmoid(np.dot(input, self.weights1.T))
            self.layer2 = sigmoid(np.dot(self.layer1, self.weights2.T))
            return sigmoid(np.dot(self.layer2, self.weights3.T))
        else:
            self.layer1 = tanh(np.dot(input, self.weights1.T))
            self.layer2 = tanh(np.dot(self.layer1, self.weights2.T))
            return tanh(np.dot(self.layer2, self.weights3.T))


if __name__ == "__main__":
    camera1 = Camera(plt.figure())
    plt.ylim(0, 0.45)
    x = np.linspace(-50, 50, 26)
    y = x ** 2
    y = y / np.linalg.norm(y)
    plt.yticks(y, "")
    x = x.reshape((-1, 1))
    x = np.c_[x, np.ones(len(x))]

    nn = NeuralNetwork(x, y)
    print("Training with sigmoid")

    for i in range(80001):
        nn.feed_forward()
        nn.back_prop()
        if i % 200 == 0:
            points = np.c_[np.linspace(-50, 50, 26), nn.output].T
            plt.scatter(*points, c="black")
            plt.text(-52., 0.45, 'Iteration: {} error: {}'
                     .format(i, error(nn.output, nn.y)), fontsize=12)

            camera1.snap()
    print("Ended training, waiting for closing animation")
    animation = camera1.animate()
    plt.show()

    x_l = np.linspace(-50, 50, 101)
    x = x_l.reshape(-1, 1)
    x = np.c_[x, np.ones(len(x_l))]
    a = nn.predict(x)
    plt.yticks(y, "")
    plt.scatter(x_l, nn.predict(x), c='b', label='Neural network')
    plt.scatter(np.linspace(-50, 50, 26), y, c='g', label='Real data')
    plt.text(-52., 0.45, 'Error: {}'
             .format(error(nn.output, nn.y)), fontsize=12)
    plt.legend(loc='best')
    plt.show()

    camera2 = Camera(plt.figure())
    plt.ylim(0.3, 0.7)
    x = np.linspace(0, 2, 21)
    y = np.sin((3 * np.pi / 2) * x)
    y = (y / np.linalg.norm(y) + 1) / 2
    plt.yticks(y, "")
    x = x.reshape((len(x), 1))
    x = np.c_[x, np.ones(len(x))]

    nn = NeuralNetwork(x, y, sygmoid=True)
    print("Training with sigmoid")
    for i in range(100001):
        nn.feed_forward()
        nn.back_prop()
        if i % 1000 == 0:
            points = np.c_[np.linspace(0, 2, 21), nn.output].T
            plt.scatter(*points, c="b")
            plt.text(0.1, 0.7, 'Iteration: {} error: {}'
                     .format(i, error(nn.output, nn.y)), fontsize=12)
            camera2.snap()
    animation = camera2.animate()
    plt.show()

    x_l = np.linspace(0, 2, 161)
    x = x_l.reshape(len(x_l), 1)
    x = np.c_[x, np.ones(len(x_l))]
    plt.yticks(y, "")

    plt.scatter(x_l, nn.predict(x), c='b', label='Neural network')
    plt.scatter(np.linspace(0, 2, 21), y, c='g', label='Real data')
    plt.text(0.1, 0.7, 'Error: {}'
             .format(error(nn.output, nn.y)), fontsize=12)
    plt.legend(loc='best')
    plt.show()
