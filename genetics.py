from network import *
import numpy as np

def breed(parentA, parentB):
    layer1A = parentA.layer1
    layer1B = parentB.layer1
    weights1A = layer1A.weights
    biases1A = layer1A.biases
    weights1B = layer1B.weights
    biases1B = layer1B.biases
    childWeights1 = []
    childBiases1 = []
    for i in range(len(weights1A)):
        heads = np.random.choice(True, False)
        if heads:
            childWeights1.append(weights1A[i])
        else:
            childWeights1.append(weights1B[i])
        heads = np.random.choice(True, False)
        if heads:
            childBiases1.append(biases1A[i])
        else:
            childBiases1.append(biases1B[i])

    layer2A = parentA.layer2
    layer2B = parentB.layer2
    weights2A = layer2A.weights
    biases2A = layer2A.biases
    weights2B = layer2B.weights
    biases2B = layer2B.biases
    childWeights2 = []
    childBiases2 = []
    for i in range(len(weights2A)):
        heads = np.random.choice(True, False)
        if heads:
            childWeights2.append(weights2A[i])
        else:
            childWeights2.append(weights2B[i])
        heads = np.random.choice(True, False)
        if heads:
            childBiases2.append(biases2A[i])
        else:
            childBiases2.append(biases2B[i])
    return [childWeights1, childBiases1, childWeights2, childBiases2]