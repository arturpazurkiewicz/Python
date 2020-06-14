import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from neural_network import NeuralNetwork, error

if __name__ == "__main__":
    camera1 = Camera(plt.figure())
    plt.ylim(0, 0.45)
    x = np.linspace(-50, 50, 26)
    y = x ** 2
    y = y / np.linalg.norm(y)
    plt.yticks(y, "")
    x = x.reshape((-1, 1))
    x = np.c_[x, np.ones(len(x))]

    nn = NeuralNetwork(x, y, layer_size=10, layer1='sigmoid',
                       layer2='sigmoid')
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
    x = x_l.reshape(len(x_l), 1)
    x = np.c_[x, np.ones(len(x_l))]

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

    nn = NeuralNetwork(x, y, layer_size=10, layer1='tanh',
                       layer2='tanh')
    print("Training with tanh")
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
