import numpy as np

class NeuralNetwork:

    def __init__(self, input_size, hidden_architecture, hidden_activation, output_activation):
        self.input_size = input_size
        # hidden_architecture is a tuple with the number of neurons in each hidden layer
        # e.g. (5, 2) corresponds to a neural network with 2 hidden layers in which the first has 5 neurons and the second has 2
        self.hidden_architecture = hidden_architecture
        # The activations are functions 
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

    def compute_num_weights(self):
        numWeights = 0
        input_size = self.input_size
        for n in self.hidden_architecture:
            numWeights = numWeights + (input_size + 1) * n
            input_size = n
        return numWeights

    def load_weights(self, weights):
        w = np.array(weights)

        self.hidden_weights = []
        self.hidden_biases = []

        start_w = 0
        input_size = self.input_size
        for n in self.hidden_architecture:
            end_w = start_w + (input_size + 1) * n
            self.hidden_biases.append(w[start_w:start_w+n])
            self.hidden_weights.append(w[start_w+n:end_w].reshape(input_size, n))
            start_w = end_w
            input_size = n

        self.output_bias = w[start_w]
        self.output_weights = w[start_w+1:]

    def forward(self, x):
        for w, b in zip(self.hidden_weights, self.hidden_biases):
            z = np.dot(x, w) + b
            x = self.hidden_activation(z)

        output_z = np.dot(x, self.output_weights) + self.output_bias
        output = self.output_activation(output_z)
        return output

def create_network_architecture(input_size):
    #hidden_architecture = (1) perceptrão simples
    hidden_architecture = (input_size // 2) #feedforward network, com uma camada escondida

    hidden_fn = lambda x: 1 / (1 + np.exp(-x))
    output_fn = lambda x: 1 if x > 0 else -1
    return NeuralNetwork(input_size, hidden_architecture, hidden_fn, output_fn)