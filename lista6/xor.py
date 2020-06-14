#!/usr/bin/python3
from neural_network import *


def create_all_models(x, y):
    return [NeuralNetwork(x, y, xor=True, layer1='sigmoid', layer2='sigmoid'),
            NeuralNetwork(x, y, xor=True, layer1='sigmoid', layer2='relu'),
            NeuralNetwork(x, y, xor=True, layer1='relu', layer2='sigmoid',
                          eta=0.9),
            NeuralNetwork(x, y, xor=True, layer1='relu', layer2='relu',
                          eta=0.08)]
    # return [NeuralNetwork(x,y,layer1='relu',layer2='sigmoid')]


def result_printer(name, network):
    print('*---*', 'Model', name, '*---*')
    print('Expected:\n', network[0].y, '\n')
    for model in network:
        print('Layer1:', model.l1, '\nLayer2:', model.l2)
        print(model.output)
        print('Error: ', float(sum((model.output - model.y) ** 2)), '\n')


if __name__ == '__main__':
    # Last column values '1' are called bias. This makes it possible to move
    # the activation of neuron
    x_xor = np.array([[0, 0, 1],
                      [0, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]])
    y_xor = np.array([[0], [1], [1], [0]])
    xor_network = create_all_models(x_xor, y_xor)

    x_and = np.array([[0, 0, 1],
                      [0, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]])
    y_and = np.array([[0], [0], [0], [1]])
    and_network = create_all_models(x_and, y_and)

    x_or = np.array([[0, 0, 1],
                     [0, 1, 1],
                     [1, 0, 1],
                     [1, 1, 1]])
    y_or = np.array([[0], [1], [1], [1]])
    or_network = create_all_models(x_or, y_or)
    print('Calculating')
    np.set_printoptions(precision=3, suppress=True)
    for network in xor_network + and_network + or_network:
        for i in range(50000):
            network.feed_forward()
            network.back_prop()

    result_printer('XOR', xor_network)
    result_printer('AND', and_network)
    result_printer('OR', or_network)
