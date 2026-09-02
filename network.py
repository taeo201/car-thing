import numpy as np
#import nnfs
#from nnfs.datasets import spiral_data

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def __str__(self):
        return f"[{self.weights}, {self.biases}]"
    
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLu:
    def __init__(self):
        pass
    def forward(self, input):
        self.output = np.maximum(0, input)

class Activation_Tanh:
    def __init__(self):
        pass
    def forward(self, input):
        self.output = np.tanh(input)

class TwoLayerNetwork:
    def __init__(self, n_inputs, n_neurons, n_outputs):
        self.layer1 = Layer_Dense(n_inputs, n_neurons)
        self.layer2 = Layer_Dense(n_neurons, n_neurons)
        self.outputLayer = Layer_Dense(n_neurons, n_outputs)
        self.activation1 = Activation_ReLu()
        self.activation2 = Activation_Tanh()

    def __str__(self):
        return f"[{self.layer1}, {self.layer2}, {self.outputLayer}]"

    
    
    def forward(self, X):
        self.layer1.forward(X)
        self.activation1.forward(self.layer1.output)
        self.layer2.forward(self.activation1.output)
        self.activation1.forward(self.layer2.output)
        self.outputLayer.forward(self.activation1.output)
        self.activation2.forward(self.outputLayer.output)
        self.output = self.activation2.output
        return self.activation2.output

if __name__ == "__main__":
    nnfs.init()

    X = [[1, 2, 3, 2.5],
            [2.0, 5.0, -1.0, 2.0],
            [-1.5, 2.7, 3.3, -0.8]
            ]

    X, y = spiral_data(100, 3)


'''
activation1 = Activation_ReLu()
activation2 = Activation_Tanh()


layer1 = Layer_Dense(2, 5)
layer2 = Layer_Dense(5, 1)
layer1.forward(X)
activation2.forward(layer1.output)
layer2.forward(activation2.output)
activation2.forward(layer2.output)
print(activation2.output)
'''















'''
weights = [[0.2, 0.8, -0.5, 1.0], 
           [0.5, -0.91, 0.26, -0.5], 
           [-0.26, -0.27, 0.17, 0.87]]
biases = [2, 3, 0.5]

weights2 = [[0.1, -0.14, 0.5],
          [-0.5, 0.12, -0.33],
          [-0.44, 0.73, -0.13]]
biases2 = [-1, 2, -0.5]

layer1_outputs = np.dot(inputs, np.array(weights).T) + biases

layer2_outputs = np.dot(layer1_outputs, np.array(weights2).T) + biases2

print(layer2_outputs)


n1 = Neuron(inputs, weights[0], biases[0])
n2 = Neuron(inputs, weights[1], biases[1])
n3 = Neuron(inputs, weights[2], biases[2])

print([n1.getOutput(), n2.getOutput(), n3.getOutput()])
'''