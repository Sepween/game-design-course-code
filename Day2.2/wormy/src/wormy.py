import random,pygame, sys
from pygame.locals import *

# Basic Setup
FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0;    # Window width and window height 
assert WINDOWHEIGHT % CELLSIZE == 0;   # must be the multiple of cellsize
CELLWIDTH = int(WINDOWWIDTH/CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE)

# Define Colors
BLACK        = (  0,   0,   0)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
DARKGREEN    = (  0, 155,   0)
DARKGRAY     = ( 40,  40,  40)
BLUE         = (  0,   0, 255)
YELLOW       = (255, 255,   0)
CYAN         = (  0, 255, 255)
PURPLE       = (138,  43, 226)
PINK         = (255, 192, 203)
BGCOLOR = BLACK

# Key Input = Worm Direction
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # The index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, HIGHEST, IFHIGHEST, SELECT
    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    HIGHEST = 0
    SELECT = pygame.mixer.Sound('Select.wav')
    pygame.display.set_caption('Wormy')

    while True:
        showStartScreen()
        color = changeColor()
        countDown()
        score = runGame(color)
        HIGHEST, IFHIGHEST = updateHighest(score)
        showGameOverScreen()

def showStartScreen():
    DISPLAYSURF.fill(BGCOLOR)

    titleFont = pygame.font.Font('freesansbold.ttf', 120)
    titleSurf = titleFont.render('WORMY', True, WHITE)
    titleRect = titleSurf.get_rect()
    titleRect.midtop = (WINDOWWIDTH/2, 110)

    startGameFont = pygame.font.Font('freesansbold.ttf', 25)
    startGameSurf = startGameFont.render('\"s\" To Start', True, WHITE)
    startGameRect = startGameSurf.get_rect()
    startGameRect.midtop = (WINDOWWIDTH/2, 245)

    quitFont = pygame.font.Font('freesansbold.ttf', 15)
    quitSurf = quitFont.render('\"ESC\" To Quit', True, WHITE)
    quitRect = quitSurf.get_rect()
    quitRect.midbottom = (WINDOWWIDTH/2, 470)

    highestFont = pygame.font.Font('freesansbold.ttf', 25)
    highestSurf = highestFont.render('Your highest is: ' + str(HIGHEST), True, WHITE)
    highestRect = highestSurf.get_rect()
    highestRect.midbottom = (WINDOWWIDTH/2, 440)

    DISPLAYSURF.blit(titleSurf, titleRect)
    DISPLAYSURF.blit(startGameSurf, startGameRect)
    DISPLAYSURF.blit(quitSurf, quitRect)
    DISPLAYSURF.blit(highestSurf, highestRect)

    pygame.display.update()
    pygame.time.wait(500)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_s):
                    pygame.mixer.Sound.play(SELECT)
                    return
                elif (event.key == K_ESCAPE):
                    terminate()

def countDown():
    while True:
        pygame.time.wait(100)
        for i in range(3, 0, -1):
            pygame.display.update()
            FPSCLOCK.tick(2)
            DISPLAYSURF.fill(BGCOLOR)
            pygame.mixer.Sound.play(SELECT)
            countDownFont = pygame.font.Font('freesansbold.ttf', 200)
            countDownSurf = countDownFont.render(str(i), True, WHITE)
            countDownRect = countDownSurf.get_rect()
            countDownRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            DISPLAYSURF.blit(countDownSurf, countDownRect)
            pygame.display.update()
            FPSCLOCK.tick(2)
        return

def changeColor():
    DISPLAYSURF.fill(BGCOLOR)

    setColorFont = pygame.font.Font('freesansbold.ttf', 40)
    setColorSurf = setColorFont.render('Press any number', True, WHITE)
    setColorRect = setColorSurf.get_rect()
    setColorRect.midtop = (WINDOWWIDTH/2, 50)

    setColorSurf2 = setColorFont.render('to set your worm\'s color', True, WHITE)
    setColorRect2 = setColorSurf2.get_rect()
    setColorRect2.midtop = (WINDOWWIDTH/2, 100)

    DISPLAYSURF.blit(setColorSurf, setColorRect)
    DISPLAYSURF.blit(setColorSurf2, setColorRect2)

    Surf0 = setColorFont.render('0', True, WHITE)
    Rect0 = Surf0.get_rect()
    Rect0.topleft = (50, 200)
    DISPLAYSURF.blit(Surf0, Rect0)

    Surf1 = setColorFont.render('1', True, RED)
    Rect1 = Surf1.get_rect()
    Rect1.topleft = (174, 200)
    DISPLAYSURF.blit(Surf1, Rect1)

    Surf2 = setColorFont.render('2', True, GREEN)
    Rect2 = Surf2.get_rect()
    Rect2.topleft = (298, 200)
    DISPLAYSURF.blit(Surf2, Rect2)

    Surf3 = setColorFont.render('3', True, DARKGREEN)
    Rect3 = Surf3.get_rect()
    Rect3.topleft = (422, 200)
    DISPLAYSURF.blit(Surf3, Rect3)

    Surf4 = setColorFont.render('4', True, DARKGRAY)
    Rect4 = Surf4.get_rect()
    Rect4.topleft = (546, 200)
    DISPLAYSURF.blit(Surf4, Rect4)

    Surf5 = setColorFont.render('5', True, BLUE)
    Rect5 = Surf5.get_rect()
    Rect5.topleft = (50, 300)
    DISPLAYSURF.blit(Surf5, Rect5)

    Surf6 = setColorFont.render('6', True, YELLOW)
    Rect6 = Surf6.get_rect()
    Rect6.topleft = (174, 300)
    DISPLAYSURF.blit(Surf6, Rect6)

    Surf7 = setColorFont.render('7', True, CYAN)
    Rect7 = Surf7.get_rect()
    Rect7.topleft = (298, 300)
    DISPLAYSURF.blit(Surf7, Rect7)

    Surf8 = setColorFont.render('8', True, PURPLE)
    Rect8 = Surf8.get_rect()
    Rect8.topleft = (422, 300)
    DISPLAYSURF.blit(Surf8, Rect8)

    Surf9 = setColorFont.render('9', True, PINK)
    Rect9 = Surf9.get_rect()
    Rect9.topleft = (546, 300)
    DISPLAYSURF.blit(Surf9, Rect9)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_0):
                    return WHITE
                elif (event.key == K_1):
                    return RED
                elif (event.key == K_2):
                    return GREEN
                elif (event.key == K_3):
                    return DARKGREEN
                elif (event.key == K_4):
                    return DARKGRAY
                elif (event.key == K_5):
                    return BLUE
                elif (event.key == K_6):
                    return YELLOW
                elif (event.key == K_7):
                    return CYAN
                elif (event.key == K_8):
                    return PURPLE
                elif (event.key == K_9):
                    return PINK
                    
def runGame(wormcolor):

    # Set Up Game
    fps = 15
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    direction = RIGHT
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    apple = getRandomLocation()
    score = 0

    # Sounds
    eat1 = pygame.mixer.Sound('EatApple1.wav')
    eat2 = pygame.mixer.Sound('EatApple2.wav')
    eatSound = [eat1, eat2]
    turn = pygame.mixer.Sound('Turn.wav')

    # Game Loop
    while True:

        # Event Handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    pygame.mixer.Sound.play(turn)
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    pygame.mixer.Sound.play(turn)
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    pygame.mixer.Sound.play(turn)
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    pygame.mixer.Sound.play(turn)
                    direction = DOWN
                elif (event.key == K_ESCAPE):
                    terminate()

        # Detect "Collisions" With Wall
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return score

        # Detect "Collisions" With Worm Body
        for wormSegment in wormCoords[3:]:
            if wormSegment['x'] == wormCoords[HEAD]['x'] and wormSegment['y'] == wormCoords[HEAD]['y']:
                return score

        # Detect "Collisions" With Apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            pygame.mixer.Sound.play(eatSound[random.randint(0,1)])
            if apple['ability'] == 'faster' and fps <= 21:
                fps += 3
            elif apple['ability'] == 'slower' and fps >= 9:
                fps -= 3
            apple = getRandomLocation()
        else:
            del wormCoords[-1]

        # Move The Worm
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y']-1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y']+1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x']-1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x']+1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)
        score = len(wormCoords) - 3

        # Paint On The Screen
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords, wormcolor)
        drawApple(apple)
        drawScore(score)
        drawSpeed(fps)
        pygame.display.update()
        FPSCLOCK.tick(fps)

def showGameOverScreen():
    DISPLAYSURF.fill(BGCOLOR)

    # Sounds
    fail = pygame.mixer.Sound('Fail.wav')
    win = pygame.mixer.Sound('Win.wav')
    
    if IFHIGHEST:
        pygame.mixer.Sound.play(win)
        gameFont = pygame.font.Font('freesansbold.ttf', 70)
        gameSurf = gameFont.render('Congratulations!', True, WHITE)
        gameRect = gameSurf.get_rect()
        gameRect.midtop = (WINDOWWIDTH/2, 80)

        overFont = pygame.font.Font('freesansbold.ttf', 55)
        overSurf = overFont.render('New Highest Score!', True, WHITE)
        overRect = overSurf.get_rect()
        overRect.midtop = (WINDOWWIDTH/2, gameRect.height+110)

        returnFont = pygame.font.Font('freesansbold.ttf', 18)
        returnSurf = returnFont.render('Press any button to restart', True, WHITE)
        returnRect = returnSurf.get_rect()
        returnRect.midbottom = (WINDOWWIDTH/2, 470)

        highestFont = pygame.font.Font('freesansbold.ttf', 25)
        highestSurf = highestFont.render('Your highest is: ' + str(HIGHEST), True, WHITE)
        highestRect = highestSurf.get_rect()
        highestRect.midbottom = (WINDOWWIDTH/2, 440)
        
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(highestSurf, highestRect)
    else:
        pygame.mixer.Sound.play(fail)
        gameFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameFont.render('Game', True, WHITE)
        gameRect = gameSurf.get_rect()
        gameRect.midtop = (WINDOWWIDTH/2, 55)

        overFont = pygame.font.Font('freesansbold.ttf', 150)
        overSurf = overFont.render('Over', True, WHITE)
        overRect = overSurf.get_rect()
        overRect.midtop = (WINDOWWIDTH/2, gameRect.height+70)

        returnFont = pygame.font.Font('freesansbold.ttf', 18)
        returnSurf = returnFont.render('Press any button to restart', True, WHITE)
        returnRect = returnSurf.get_rect()
        returnRect.midbottom = (WINDOWWIDTH/2, 470)

        highestFont = pygame.font.Font('freesansbold.ttf', 25)
        highestSurf = highestFont.render('Your highest is: ' + str(HIGHEST), True, WHITE)
        highestRect = highestSurf.get_rect()
        highestRect.midbottom = (WINDOWWIDTH/2, 440)
        
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(highestSurf, highestRect)

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # Clear the event cache

    while True:
        if checkForKeyPress():
            pygame.mixer.Sound.play(SELECT)
            pygame.event.get()
            return

def drawGrid():
    for x in range(0, WINDOWWIDTH-1, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0), (x,WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT-1, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH,y))

def drawWorm(wormCoords, wormcolor):
    for segment in wormCoords:
        x = segment['x'] * CELLSIZE
        y = segment['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, wormcolor, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)

def drawApple(apple):
    x = apple['x'] * CELLSIZE
    y = apple['y'] * CELLSIZE
    appleSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, apple['color'], appleSegmentRect)

def drawScore(score):
    scoreFont = pygame.font.Font('freesansbold.ttf', 18)
    scoreSurf = scoreFont.render('Score: '+str(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.top = (5)
    scoreRect.left = (5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    return

def drawSpeed(fps):
    speedFont = pygame.font.Font('freesansbold.ttf', 18)
    speedSurf = speedFont.render('Speed: '+str(int(fps/3-1)), True, WHITE)
    speedRect = speedSurf.get_rect()
    speedRect.top = (30)
    speedRect.left = (5)
    DISPLAYSURF.blit(speedSurf, speedRect)
    return

def getRandomLocation():
    all_abilities = ['faster', 'slower', 'none', 'none', 'none', 'none']
    randAbility = all_abilities[random.randint(0,len(all_abilities)-1)]
    color = None
    if randAbility == 'faster':
        color = GREEN
    elif randAbility == 'slower':
        color = YELLOW
    else:
        color = RED
    return {'x': random.randint(0, CELLWIDTH-1), 'y': random.randint(0, CELLHEIGHT-1), 'ability': randAbility, 'color': color}

def updateHighest(score):
    if score > HIGHEST:
        return score, True
    else:
        return HIGHEST, False

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            else:
                return True
    return False

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

#start game and game over screen
#choose color function
#add count down
#faster and slower abilities for apples
#highest score count
#sound