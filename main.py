from mainloop import generationRunThrough
from network import TwoLayerNetwork
from genetics import createNextGen
GENERATIONS = 50
DURATION_LIMIT = 30 #seconds
AI_NUM = 100
TOP_PERCENT = 5 #top x% breed
ELITISM = 2 #Keep top x performing models unchanged

numToBreed = (AI_NUM * TOP_PERCENT) // 100
networks = []
for i in range(GENERATIONS):

    if not networks:
        for _ in range(AI_NUM):
            networks.append(TwoLayerNetwork(8,15,5))

    carList = generationRunThrough(DURATION_LIMIT, AI_NUM, networks, i+1)
    if carList == "QUIT":
        break
    for car in carList:
        car.fitness = len(car.checkpoints)*10000 + car.distSinceLastCheckpoint

    sorted_cars = sorted(carList, key=lambda emp: emp.fitness, reverse=True)
    topNets = []
    topCars = sorted_cars[0:numToBreed]
    for car in topCars:
        topNets.append(car.net)

    networks = createNextGen(AI_NUM, topNets, ELITISM, i, GENERATIONS)

print(topNets[0])
