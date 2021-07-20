import pygame, sys, math
from pygame.locals import *
from fractions import Fraction
import numpy as np

pygame.init()

# Basic Setting Up
FPS = 60
fpsClock = pygame.time.Clock()

RESOLUTION = (800,600)
DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Bouncing Balls")

# Create Constants
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 50
SPEED = 30

# Create Variables
xDirections = ('right', 'left')
yDirections = ('up', 'down')
directionx = xDirections[np.random.randint(2)]
directiony = yDirections[np.random.randint(2)]
angle = np.random.randint(91)
posx = np.random.randint(50, 751)
posy = np.random.randint(50, 551)

font = pygame.font.Font('freesansbold.ttf', 20)
text1 = font.render('Starting direction: ' + directionx + ' ' + directiony, True, BLACK, WHITE)
textRect1 = text1.get_rect()
textRect1.top = 5
textRect1.left = 5
text2 = font.render('Starting angle: ' + str(angle) + ' degrees', True, BLACK, WHITE)
textRect2 = text2.get_rect()
textRect2.top = 35
textRect2.left = 5
text3 = font.render('Starting position: (' + str(posx) + ', ' + str(posy) + ')', True, BLACK, WHITE)
textRect3 = text3.get_rect()
textRect3.top = 65
textRect3.left = 5

# Game Loop
while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(text1, textRect1)
    DISPLAYSURF.blit(text2, textRect2)
    DISPLAYSURF.blit(text3, textRect3)

    # Determine new direction
    if posx + RADIUS >= 800:
        directionx = "left"
    elif posx - RADIUS <= 0:
        directionx = "right"
    if posy + RADIUS >= 600:
        directiony = "up"
    elif posy - RADIUS <= 0:
        directiony = "down"
  
    # Determine change of x and y
    ratioOfYtoX = math.tan(angle * math.pi / 180)
    changeToX = SPEED / (1 + ratioOfYtoX)
    changeToY = SPEED - changeToX

    # Change x and y
    if directionx == "right" and directiony == "down":
        posx += changeToX
        posy += changeToY
    elif directionx == "right" and directiony == "up":
        posx += changeToX
        posy -= changeToY
    elif directionx == "left" and directiony == "down":
        posx -= changeToX
        posy += changeToY
    elif directionx == "left" and directiony == "up":
        posx -= changeToX
        posy -= changeToY

    # Determine center and draw circle
    center = (posx, posy)
    pygame.draw.circle (DISPLAYSURF, BLUE, center, RADIUS) # Argument: (surface, color, center, radius, thickness)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    fpsClock.tick(FPS)