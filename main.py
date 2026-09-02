import pygame
from utils import *
import math
from network import *

np.random.seed(0)

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
player = Car(startingX, startingY, carWidth, carHeight, "blue")
track = Track(TRACK_PATH)
#track = Obstacle()

net = TwoLayerNetwork(8, 15, 5)

AI = Car(startingX, startingY, carWidth, carHeight, "green")
options = [AI.accelerate, AI.accelLeft, AI.accelRight, AI.turnRight, AI.turnLeft]

cars = [player, AI]

sensors = []
for car in cars:
    sensors.append(Sensor(car, track, 7))

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

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
        print(f"Sensor {i}: {distances}")
        car.distances = distances


    distances_input = AI.distances if AI.distances else [-1] * 7
    net.forward(distances_input + [AI.speed])
    output = net.output[0]
    max = -100
    maxIndex = -1
    for i in range(len(output)):
        if output[i] > max:
            max = output[i]
            maxIndex = i
    AIChoice = options[maxIndex]

    if AIChoice == AI.accelerate:
        AIChoice(ACCELERATION)
    elif AIChoice in [AI.turnLeft, AI.turnRight]:
        AIChoice(ROTATION_ACCELERATION)
    else:
        AIChoice(ACCELERATION, ROTATION_ACCELERATION)

    #player.updatePosition()
    track.draw(screen)
    for car in cars:
        if car.alive:
            car.movementTick(MAX_SPEED, MAX_ROTATION_SPEED, FRICTION_COEFF, ROT_FRICT_COEFF)
            offset_x = car.rect.x - track.rect.x
            offset_y = car.rect.y - track.rect.y
            if track.mask.overlap(car.mask, (offset_x, offset_y)):
                car.die()
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
