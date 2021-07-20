import pygame, sys, math
from pygame.locals import *

pygame.init()

def detectCollision(center1, radius1, center2, radius2):
    centerDistanceX = abs(center1[0] - center2[0])
    centerDistanceY = abs(center1[1] - center2[1])
    centerDistance = math.sqrt(centerDistanceX ** 2 + centerDistanceY ** 2)
    radiusTotal = radius1 + radius2
    if centerDistance <= radiusTotal:
        return True
    else:
        return False

def calculateVelocity(center1, velocity1, RADIUS1, center2, velocity2, RADIUS2):
    scaleFactor = (2*(velocity1[0]*(center1[0]-center2[0])+velocity1[1]*(center1[1]-center2[1])))/((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)
    velocity1[0] = (velocity1[0] - scaleFactor * (center1[0] - center2[0]))
    velocity1[1] = (velocity1[1] - scaleFactor * (center1[1] - center2[1]))

# Basic Setting Up
FPS = 60
fpsClock = pygame.time.Clock()

RESOLUTION = (800,600)
DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Bouncing Balls")

# Create Variables
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
center1 = [200, 300]
center2 = [600, 300]
velocity1 = [60, 60]
velocity2 = [-60, 60]
RADIUS1 = 100
RADIUS2 = 50

while True:
    DISPLAYSURF.fill(WHITE)

    if center1[0] + RADIUS1 >= 800 or center1[0] - RADIUS1 <= 0:
        velocity1[0] *= -1
    if center1[1] + RADIUS1 >= 600 or center1[1] - RADIUS1 <= 0:
        velocity1[1] *= -1
    if center2[0] + RADIUS2 >= 800 or center2[0] - RADIUS2 <= 0:
        velocity2[0] *= -1
    if center2[1] + RADIUS2 >= 600 or center2[1] - RADIUS2 <= 0:
        velocity2[1] *= -1

    if detectCollision(center1, RADIUS1, center2, RADIUS2):
        calculateVelocity(center1, velocity1, RADIUS1, center2, velocity2, RADIUS2)
        calculateVelocity(center2, velocity2, RADIUS2, center1, velocity1, RADIUS1)

    speed1 = [velocity1[0]/FPS, velocity1[1]/FPS]
    speed2 = [velocity2[0]/FPS, velocity2[1]/FPS]

    center1[0] += speed1[0]
    center1[1] += speed1[1]
    center2[0] += speed2[0]
    center2[1] += speed2[1]

    pygame.draw.circle (DISPLAYSURF, BLUE, center1, RADIUS1) # Argument: (surface, color, center, radius, thickness)
    pygame.draw.circle (DISPLAYSURF, RED, center2, RADIUS2) # Argument: (surface, color, center, radius, thickness)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    fpsClock.tick(FPS)