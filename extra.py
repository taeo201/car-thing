import numpy as np
class Neuron:
    def __init__(self, inputs, weights, bias):
        self.output = np.dot(weights, inputs) + bias

    def getOutput(self):
        return float(self.output)
