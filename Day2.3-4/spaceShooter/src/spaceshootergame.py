# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 11:26:21 2019

@author: J. Tyler McGoffin
"""

import pygame, sys
import numpy as np
from pygame.locals import *

from ship import Ship
from laser import Laser
from asteroid import Asteroid
from background import Background

#Set up window and frame rate variables
FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 700

#Set up some Color variables
BLACK = (0, 0, 0)
NAVYBLUE = (0, 0, 128)
DARKPURPLE = (100, 0, 100)
WHITE = (255, 255, 255)
DARKGRAY = (100, 100, 100)

#Start the game
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT #True globals
    
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Space Shooter")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def showStartScreen():
    return

def runGame():
    # setup the game
    score = 0 # number of asteroids destroyed
    lives = 3
    levelUp = False

    # create game objects: ship, asteroids, lasers, background
    # ship controls
    playerShip = Ship(WINDOWWIDTH, WINDOWHEIGHT)
    leftHeld = False
    rightHeld = False
    upHeld = False
    downHeld = False
    firing = False

    # lasers
    lasers = initializeObjects(10)
    laserIndex = 0
    laserSpeed = 10
    fireRate = 4

    # asteroid stuff
    asteroids = initializeObjects(25)
    spawnRate = 1 # on average, we'll spawn 1 asteroid per second
    minAsteroidSpeed = 1
    maxAsteroidSpeed = 6
    asteroidIndex = 0


    # backgrounds
    backgroundObject = Background("background", WINDOWHEIGHT)
    paralaxObject = Background("paralax", WINDOWHEIGHT)

    # game loop
    while True:
        # event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_a or event.key == K_LEFT:
                    leftHeld = True
                elif event.key == K_d or event.key == K_RIGHT:
                    rightHeld = True
                elif event.key == K_w or event.key == K_UP:
                    upHeld = True
                elif event.key == K_s or event.key == K_DOWN:
                    downHeld = True
                elif event.key == K_SPACE:
                    firing = True
            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_LEFT:
                    leftHeld = False
                elif event.key == K_d or event.key == K_RIGHT:
                    rightHeld = False
                elif event.key == K_w or event.key == K_UP:
                    upHeld = False
                elif event.key == K_s or event.key == K_DOWN:
                    downHeld = False
                elif event.key == K_SPACE:
                    firing = False
        # increase game difficulty
        if score % 10 == 0 and levelUp:
            minAsteroidSpeed += 2
            maxAsteroidSpeed += 2
            spawnRate += 1
            levelUp = False
        elif score % 10 != 0:
            levelUp = True
        # spawn asteroids and lasers
        if firing:
            lasers[laserIndex] = Laser(playerShip.rect, laserSpeed)
            firing = False
            laserIndex += 1
            if laserIndex >= len(lasers):
                laserIndex = 0

        # automate asteroid spawing
        if np.random.randint(0, FPS/spawnRate) == 0:
            asteroids[asteroidIndex] = Asteroid(WINDOWWIDTH, WINDOWHEIGHT, np.random.randint(minAsteroidSpeed, maxAsteroidSpeed))
            asteroidIndex += 1
            if asteroidIndex >= len(asteroids):
                asteroidIndex = 0
        # detect collisions

        # update state
        playerShip.move (left=leftHeld, right=rightHeld, up=upHeld, down=downHeld)
        backgroundObject.move()
        paralaxObject.move()
        for laser in lasers:
            if laser != None:
                laser.move()
        for asteroid in asteroids:
            if asteroid != None:
                asteroid.move()

        # detect collisions
        for currentAsteroidIndex, asteroid in enumerate(asteroids):
            if asteroid != None:
                for currentLaserIndex, laser in enumerate(lasers):
                    if laser != None:
                        if laser.rect.colliderect(asteroid.rect):
                            asteroids[currentAsteroidIndex] = None
                            lasers[currentLaserIndex] = None
                            score += 1
                if playerShip.rect.colliderect(asteroid.rect):
                    lives -= 1
                    if lives > 0:
                        # reset code
                        playerHit()
                        playerShip.setStartPos()
                        asteroids = initializeObjects(25)
                        lasers = initializeObjects(10)
                    else:
                        return
                    break

        # draw on screen
        DISPLAYSURF.fill(BLACK)
        draw(imageSurf = backgroundObject.image, imageRect = backgroundObject.rect)
        draw(imageSurf = paralaxObject.image, imageRect = paralaxObject.rect)
        draw(imageSurf = playerShip.image, imageRect = playerShip.rect) # args = image, rect
        drawLasers(lasers)
        drawAsteroids(asteroids)
        drawHUD(lives, score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def showGameOverScreen():
    return

def initializeObjects(number):
    objects = []
    for x in range(number):
        objects.append(None)
    return objects

def playerHit():
    hitSurf = BASICFONT.render("You've been destroyed!", True, WHITE)
    hitRect = hitSurf.get_rect()
    hitRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    draw(hitSurf, hitRect)

    pygame.display.update()
    pygame.time.wait(2000)

def drawLasers(lasers):
    for laser in lasers:
        if laser != None:
            draw(laser.image, laser.rect)

def drawAsteroids(asteroids):
    for asteroid in asteroids:
        if asteroid != None:
            image, rect = asteroid.draw()
            draw(image, rect)

def draw(imageSurf, imageRect):
    DISPLAYSURF.blit(imageSurf, imageRect)

def drawHUD(lives, score):
    healthBarSurf = BASICFONT.render("Ship remaining: " + str(lives), True, WHITE)
    healthBarRect = healthBarSurf.get_rect()
    healthBarRect.topleft = (10,10)
    draw(healthBarSurf, healthBarRect)

    scoreSurf = BASICFONT.render("Asteroids destroyed: " + str(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH-10, 10)
    draw(scoreSurf, scoreRect)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()