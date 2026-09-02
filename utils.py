import pygame
import math

class Car:
    def __init__(self, x, y, w, h, colour, net=None, simple=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        self.rotation = 0
        self.speed = 0
        self.rotationSpeed = 0
        self.simpleRotSpeed = 3
        self.alive = True
        self.simple = simple
        self.sensor = None
        self.distances = []
        self.net = net
        self.checkpoints = []
        self.distSinceLastCheckpoint = 0
        self.fitness = 0

        self.prevPos = (x, y)

        self.surface = pygame.Surface((w, h))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.fill(self.colour)

        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.Mask((w, h))
        self.mask.fill()

    def movementTick(self, MAX_SPEED, MAX_ROTATION_SPEED, FRICTION_COEFF, ROT_FRICT_COEFF):
        self.speed = self.speed - self.speed*FRICTION_COEFF

        if not self.simple:
            self.rotationSpeed = self.rotationSpeed - self.rotationSpeed*ROT_FRICT_COEFF


        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED
        elif self.speed < -MAX_SPEED:
            self.speed = -MAX_SPEED
        elif -0.1 <= self.speed <= 0.1:
            self.speed = 0

        if not self.simple:
            if self.rotationSpeed > MAX_ROTATION_SPEED:
                self.rotationSpeed = MAX_ROTATION_SPEED
            elif self.rotationSpeed < -MAX_ROTATION_SPEED:
                self.rotationSpeed = -MAX_ROTATION_SPEED
            elif -0.1 <= self.rotationSpeed <= 0.1:
                self.rotationSpeed = 0
            self.rotation += self.rotationSpeed
        else:
            #self.rotation += self.simpleRotSpeed
            pass

        self.rotation = self.rotation % -360
        rotation_radians = self.rotation * math.pi / 180


        ySpeed = self.speed * math.cos(rotation_radians)
        xSpeed = self.speed * math.sin(rotation_radians)
    
        self.y -= ySpeed
        self.x -= xSpeed

        totalSpeed = math.sqrt(xSpeed**2 + ySpeed**2)
        self.distSinceLastCheckpoint += totalSpeed

        rotated_surface = pygame.transform.rotate(self.surface, self.rotation)
        self.rect = rotated_surface.get_rect()
        self.rect.center = (self.x, self.y)

        self.mask = pygame.mask.from_surface(rotated_surface)
        #self.mask = pygame.mask.Mask((self.w, self.h))
        #self.mask.fill()

    def accelerate(self, ACCELERATION):
        self.speed += ACCELERATION

    def accelLeft(self, ACCELERATION, ROTATION_ACCELERATION):
        self.accelerate(ACCELERATION)
        self.turnLeft(ROTATION_ACCELERATION)

    def accelRight(self, ACCELERATION, ROTATION_ACCELERATION):
        self.accelerate(ACCELERATION)
        self.turnRight(ROTATION_ACCELERATION)

    def rotAccelerate(self, ROTATION_ACCELERATION):
        self.rotationSpeed += ROTATION_ACCELERATION * math.copysign(1, self.speed)

    def draw(self, screen):
        self.surface.fill(self.colour)
        rotated_surface = pygame.transform.rotate(self.surface, self.rotation)
        screen.blit(rotated_surface, self.rect)

    def reset(self, startingX, startingY):
        (self.x, self.y) = (startingX, startingY)
        self.speed = 0
        self.rotation = 0
        self.rotationSpeed = 0
        self.alive = True

    def die(self):
        self.alive = False
        self.colour = "dark gray"

    def turnLeft(self, ROTATION_ACCELERATION):
        if self.alive:
            if self.simple:
                self.rotation += self.simpleRotSpeed
            else:
                self.rotAccelerate(ROTATION_ACCELERATION)

    def turnRight(self, ROTATION_ACCELERATION):
        if self.alive:
            if self.simple:
                self.rotation -= self.simpleRotSpeed
            else:
                self.rotAccelerate(-ROTATION_ACCELERATION)

    def baccel(self, ACCELERATION):
        self.accelerate(-ACCELERATION)

class Sensor:
    def __init__(self, car, track, raycount):
        self.car = car
        self.car.sensor = self
        self.track = track
        self.rayCount = raycount
        self.maxLength = 100
        self.rayAngles = []
        for i in range(self.rayCount):
            self.rayAngles.append(self.getRayAngle(i))

    def getRayAngle(self, rayN):
        A = -90
        B = 90
        t = rayN / (self.rayCount - 1)
        angle = A + (B-A) * t
        return angle

    def updateSensors(self, screen):
        self.x, self.y = (self.car.x, self.car.y)
        collisions = []
        distances = []
        i = 0
        #print(self.rayAngles)
        for rayAngle in self.rayAngles:
            collisions.append(self.castRay(rayAngle, screen, i))
            i += 1
        for collision in collisions:
            if collision != -1:
                distances.append(math.sqrt((self.x - collision[0])**2 + (self.y-collision[1]) ** 2))
                
            else:
                distances.append(-1)
        return distances[::-1]


    def castRay(self, angle, screen, i, step=1):
        newAngle = angle + self.car.rotation
        newAngleRad = math.radians(newAngle)
        #print(self.car.rotation)
        #if angle == -90:
        #print(angle, newAngle)
        dx = math.sin(newAngleRad) * step
        dy = math.cos(newAngleRad) * step

        current_x, current_y = self.x, self.y

        
        collided = False
        l = 0

        for _ in range(0, self.maxLength, step):
            current_x -= dx
            current_y -= dy
            l += step
            #if self.track.collidepoint(current_x, current_y):
                #return (int(current_x), int(current_y))
            local_x = current_x - self.track.rect.x
            local_y = current_y - self.track.rect.y
            if 0 <= local_x < self.track.rect.width and 0 <= local_y < self.track.rect.height:
                if self.track.mask.get_at((int(local_x), int(local_y))):
                    collided = True
                    break

        self.surface = pygame.Surface((1, l))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.fill("yellow")
        rotated_surface = pygame.transform.rotate(self.surface, newAngle)
        self.rect = rotated_surface.get_rect()
        self.rect.center = ((self.x - math.sin(newAngleRad) * l / 2), (self.y - math.cos(newAngleRad) * l / 2))
        screen.blit(rotated_surface, self.rect)
        
        if collided:
            return (int(current_x), int(current_y))
        else:
            return -1

class Track:
    def __init__(self, PATH):
        self.image = pygame.image.load(PATH).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (0,0))

class Obstacle:
    def __init__(self):
        self.w, self.h = 20, 20
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.fill("red")

        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.Mask((self.w, self.h))
        self.mask.fill()

    def draw(self, screen):
        self.rect.center = pygame.mouse.get_pos()
        screen.blit(self.surface, self.rect)

class Checkpoint:
    def __init__(self, x, y, rot, w, h, ID, carList):
        self.x, self.y = x, y
        if rot == 0:
            self.w, self.h = w, h
        elif rot == 90:
            self.w, self.h = h, w
        self.id = ID
        self.carList = carList
        #print(self.carList)
        #print(self.carList[0].x, self.carList[0].y)

        self.surface = pygame.Surface((self.w, self.h))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.fill("dark green")

        self.rect = self.surface.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pygame.mask.Mask((self.w, self.h))
        self.mask.fill()

    def draw(self, SCREEN):
        SCREEN.blit(self.surface, self.rect)

    def checkForCars(self, TOTALCHECKPOINTS):
        for car in self.carList:
            if self.rect.colliderect(car.rect):
                car.distSinceLastCheckpoint = 0
                if not car.checkpoints:
                    if self.id == 0:
                        car.checkpoints.append(self.id)
                    else:
                        car.die()
                else:
                    if car.checkpoints[-1] == (self.id -1) % TOTALCHECKPOINTS:
                        car.checkpoints.append(self.id)
                    elif car.checkpoints[-1] == self.id:
                        pass
                    else:
                        car.die()
                        #car.checkpoints = []

