from network import *
from network import TwoLayerNetwork
import numpy as np

def breed(parentA, parentB):
    child = TwoLayerNetwork(8, 15, 5)
    layer1A = parentA.layer1
    layer1B = parentB.layer1
    weights1A = layer1A.weights
    biases1A = layer1A.biases
    weights1B = layer1B.weights
    biases1B = layer1B.biases

    

    for i in range(len(weights1A)):
        for j in range(len(weights1A[i])):
            if np.random.choice([True, False]):
                child.layer1.weights[i][j] = weights1A[i][j]
            else:
                child.layer1.weights[i][j] = weights1B[i][j]
    
    for i in range(len(biases1A[0])):
        if np.random.choice([True, False]):
            child.layer1.biases[0][i] = biases1A[0][i]
        else:
            child.layer1.biases[0][i] = biases1B[0][i]

    layer2A = parentA.layer2
    layer2B = parentB.layer2
    weights2A = layer2A.weights
    biases2A = layer2A.biases
    weights2B = layer2B.weights
    biases2B = layer2B.biases

    for i in range(len(weights2A)):
        for j in range(len(weights2A[i])):
            if np.random.choice([True, False]):
                child.layer2.weights[i][j] = weights2A[i][j]
            else:
                child.layer2.weights[i][j] = weights2B[i][j]
    
    for i in range(len(biases2A[0])):
        if np.random.choice([True, False]):
            child.layer2.biases[0][i] = biases2A[0][i]
        else:
            child.layer2.biases[0][i] = biases2B[0][i]

    weightsOutA = parentA.outputLayer.weights
    biasesOutA = parentA.outputLayer.biases
    weightsOutB = parentB.outputLayer.weights
    biasesOutB = parentB.outputLayer.biases
    
    for i in range(len(weightsOutA)):
        for j in range(len(weightsOutA[i])):
            if np.random.choice([True, False]):
                child.outputLayer.weights[i][j] = weightsOutA[i][j]
            else:
                child.outputLayer.weights[i][j] = weightsOutB[i][j]
    
    for i in range(len(biasesOutA[0])):
        if np.random.choice([True, False]):
            child.outputLayer.biases[0][i] = biasesOutA[0][i]
        else:
            child.outputLayer.biases[0][i] = biasesOutB[0][i]

    return child

def mutateHelper(layer, strength, chance):
    weights = layer.weights
    biases = layer.biases

    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if np.random.randint(1, chance+1) == 1:
                mutation = np.random.normal(0, strength)
                weights[i][j] += mutation
    for i in range(len(biases[0])):
        if np.random.randint(1, chance+1) == 2:
            mutation = np.random.normal(0, strength)
            biases[0][i] += mutation
    return weights, biases

def mutate(net):
    chance = 10 # 1/x chance of mutation
    strength = 0.2

    layer1 = net.layer1
    weights1, biases1 = mutateHelper(layer1, strength, chance)
    net.layer1.weights = weights1
    net.layer1.biases = biases1

    layer2 = net.layer2
    weights2, biases2 = mutateHelper(layer2, strength, chance)
    net.layer2.weights = weights2
    net.layer2.biases = biases2

    outputLayer = net.outputLayer
    weightsOut, biasesOut = mutateHelper(outputLayer, strength, chance)
    net.outputLayer.weights = weightsOut
    net.outputLayer.biases = biasesOut

    return net

def createNextGen(popSize, parents, ELITISM):
    children = parents[0:ELITISM]

    while len(children) < popSize:
        child = breed(np.random.choice(parents), np.random.choice(parents))
        child = mutate(child)
        children.append(child)
    return children