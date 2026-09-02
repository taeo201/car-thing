import pygame
from utils import *
import math
from network import *
from genetics import *
import time

#np.random.seed(0)

pygame.init()
X = 1280
Y = 720
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
FPS = 60

MAX_SPEED = 5
ACCELERATION = 0.5
ROTATION_ACCELERATION = 1
MAX_ROTATION_SPEED = 5
FRICTION_COEFF = 0.05
ROT_FRICT_COEFF = 0.25
TRACK_PATH = "Tracks\\Track1.png"
carWidth = 25
carHeight = 50
startingX, startingY = (155, 310)
track = Track(TRACK_PATH)

checkpoint_locations = [(155, 250, 0), 
                        (283, 90, 90),
                        (518, 257, 90), 
                        (812, 300, 90), 
                        (1055, 396, 0),
                        (790, 470, 90),
                        (541, 655, 90),
                        (326, 495, 90),
                        (170, 414, 0)
                        ]
TOTALCHECKPOINTS = len(checkpoint_locations)
checkpoints = []

def generationRunThrough(DURATION_LIMIT, AI_NUM):
    player = Car(startingX, startingY, carWidth, carHeight, "blue")
    livingCars = [player]
    cars = [player]
    for i in range(AI_NUM):
        newCar = Car(startingX, startingY, carWidth, carHeight, "green", TwoLayerNetwork(8,15,5))
        cars.append(newCar)
        livingCars.append(newCar)

    player.die()
    sensors = []
    for car in cars:
        sensors.append(Sensor(car, track, 7))

    id = 0
    for checkpoint in checkpoint_locations:
        checkpoints.append(Checkpoint(checkpoint[0], checkpoint[1], checkpoint[2], 110, 50, id, cars))
        id +=1


    startTime = time.perf_counter()
    cont = True
    while cont:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.turnLeft(ROTATION_ACCELERATION)
        if keys[pygame.K_d]:
            player.turnRight(ROTATION_ACCELERATION)
        if keys[pygame.K_w]:
            player.accelerate(ACCELERATION)
        if keys[pygame.K_s]:
            player.baccel(ACCELERATION)
        if keys[pygame.K_RIGHT]:
            player.rotation = 90
        if keys[pygame.K_SPACE]:
            for car in cars:
                print(car.checkpoints)
                car.reset(startingX, startingY)
        if keys[pygame.K_ESCAPE]:
            print(player.x, player.y)
            pygame.quit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("light gray")


        # RENDER YOUR GAME HERE
        i = 0
        for car in cars:
            i+= 1
            distances = car.sensor.updateSensors(screen)
            #print(f"Sensor {i}: {distances}")
            car.distances = distances

            if car != player:
                options = [car.accelerate, car.accelLeft, car.accelRight, car.turnRight, car.turnLeft]
                distances_input = [x / 100 for x in car.distances]
                car.net.forward(distances_input + [car.speed/100])
                output = car.net.output[0]
                max = -100
                maxIndex = -1
                for j in range(len(output)):
                    if output[j] > max:
                        max = output[j]
                        maxIndex = j
                AIChoice = options[maxIndex]

                if AIChoice == car.accelerate:
                    AIChoice(ACCELERATION)
                elif AIChoice in [car.turnLeft, car.turnRight]:
                    AIChoice(ROTATION_ACCELERATION)
                else:
                    AIChoice(ACCELERATION, ROTATION_ACCELERATION)

        #player.updatePosition()
        track.draw(screen)
        for checkpoint in checkpoints:
            checkpoint.draw(screen)
            checkpoint.checkForCars(TOTALCHECKPOINTS)
        for car in cars:
            if car.alive:
                car.movementTick(MAX_SPEED, MAX_ROTATION_SPEED, FRICTION_COEFF, ROT_FRICT_COEFF)
                offset_x = car.rect.x - track.rect.x
                offset_y = car.rect.y - track.rect.y
                if track.mask.overlap(car.mask, (offset_x, offset_y)):
                    livingCars.remove(car)
                    car.die()
                    if not livingCars:
                        cont = False
            car.draw(screen)

        '''
        if player.alive:
            player.movementTick(MAX_SPEED, MAX_ROTATION_SPEED, FRICTION_COEFF, ROT_FRICT_COEFF)
            offset_x = player.rect.x - track.rect.x
            offset_y = player.rect.y - track.rect.y
        player.draw(screen)
        if track.mask.overlap(player.mask, (offset_x, offset_y)):
            player.die()
            '''

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS

        if time.perf_counter() - startTime > DURATION_LIMIT:
            cont = False

    return cars