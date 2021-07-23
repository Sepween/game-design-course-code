import random,pygame, sys
from pygame.locals import *
from worms import Worms
from apples import Apples

# Basic Setup
FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
WINDOWWIDTHD = 1280
WINDOWHEIGHTD = 790
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0;    # Window width and window height 
assert WINDOWHEIGHT % CELLSIZE == 0;   # must be the multiple of cellsize
CELLWIDTH = int(WINDOWWIDTH/CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE)
CELLWIDTHD = int(WINDOWWIDTHD/CELLSIZE)
CELLHEIGHTD = int(WINDOWHEIGHTD/CELLSIZE)

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

# ==========Initial Functions==========

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, HIGHEST, IFHIGHEST, SELECT, SINGLEORDOUBLE
    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    HIGHEST = 0
    SELECT = pygame.mixer.Sound('Select.wav')
    pygame.display.set_caption('Wormy')

    while True:
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        SINGLEORDOUBLE = showStartScreen()
        if SINGLEORDOUBLE == 'Single':
            while True:
                color = changeColor()
                countDown()
                score = runGame(color)
                HIGHEST, IFHIGHEST = updateHighest(score)
                next = showGameOverScreen()
                if next == 'Restart':
                    continue
                elif next == 'Main':
                   break
        elif SINGLEORDOUBLE == 'Double':
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTHD, WINDOWHEIGHTD))
            while True:
                color1 = DchangeColorP1()
                color2 = DchangeColorP2()
                DcountDown()
                reason = DrunGame(color1, color2)
                next = DshowGameOverScreen(reason)
                if next == 'Restart':
                    continue
                elif next == 'Main':
                   break

def showStartScreen():
    DISPLAYSURF.fill(BGCOLOR)

    titleFont = pygame.font.Font('freesansbold.ttf', 120)
    titleSurf = titleFont.render('WORMY', True, WHITE)
    titleRect = titleSurf.get_rect()
    titleRect.midtop = (WINDOWWIDTH/2, 80)

    startGameFont = pygame.font.Font('freesansbold.ttf', 25)
    startGameSurf = startGameFont.render('\"s\" To Start Single Player Mode', True, WHITE)
    startGameRect = startGameSurf.get_rect()
    startGameRect.midtop = (WINDOWWIDTH/2, 225)

    startDGameFont = pygame.font.Font('freesansbold.ttf', 25)
    startDGameSurf = startDGameFont.render('\"d\" To Start Double Player Mode', True, WHITE)
    startDGameRect = startDGameSurf.get_rect()
    startDGameRect.midtop = (WINDOWWIDTH/2, 265)

    quitFont = pygame.font.Font('freesansbold.ttf', 15)
    quitSurf = quitFont.render('\"ESC\" To Quit', True, WHITE)
    quitRect = quitSurf.get_rect()
    quitRect.midbottom = (WINDOWWIDTH/2, 470)

    highestFont = pygame.font.Font('freesansbold.ttf', 25)
    highestSurf = highestFont.render('Your highest (Single Player) is: ' + str(HIGHEST), True, WHITE)
    highestRect = highestSurf.get_rect()
    highestRect.midbottom = (WINDOWWIDTH/2, 380)

    DISPLAYSURF.blit(titleSurf, titleRect)
    DISPLAYSURF.blit(startGameSurf, startGameRect)
    DISPLAYSURF.blit(startDGameSurf, startDGameRect)
    DISPLAYSURF.blit(quitSurf, quitRect)
    DISPLAYSURF.blit(highestSurf, highestRect)

    pygame.display.update()
    pygame.time.wait(500)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    pygame.mixer.Sound.play(SELECT)
                    return 'Single'
                elif event.key == K_d:
                    pygame.mixer.Sound.play(SELECT)
                    return 'Double'
                elif event.key == K_ESCAPE:
                    terminate()

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
            elif event.key == K_RETURN:
                return 'Main'
            else:
                return 'Restart'
    return False

# ==========Single Player Functions==========

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

    # Heads
    whiteHead = pygame.image.load('1White.png')
    redHead = pygame.image.load('2Red.png')
    greenHead = pygame.image.load('3Green.png')
    darkGreenHead = pygame.image.load('4Dark_green.png')
    darkGrayHead = pygame.image.load('5Dark_gray.png')
    blueHead = pygame.image.load('6Blue.png')
    yellowHead = pygame.image.load('7Yellow.png')
    cyanHead = pygame.image.load('8Cyan.png')
    purpleHead = pygame.image.load('9Purple.png')
    pinkHead = pygame.image.load('10Pink.png')


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

        if wormcolor == WHITE:
            drawWorm(wormCoords, wormcolor, direction, whiteHead)
        elif wormcolor == RED:
            drawWorm(wormCoords, wormcolor, direction, redHead)
        elif wormcolor == GREEN:
            drawWorm(wormCoords, wormcolor, direction, greenHead)
        elif wormcolor == DARKGREEN:
            drawWorm(wormCoords, wormcolor, direction, darkGreenHead)
        elif wormcolor == DARKGRAY:
            drawWorm(wormCoords, wormcolor, direction, darkGrayHead)
        elif wormcolor == BLUE:
            drawWorm(wormCoords, wormcolor, direction, blueHead)
        elif wormcolor == YELLOW:
            drawWorm(wormCoords, wormcolor, direction, yellowHead)
        elif wormcolor == CYAN:
            drawWorm(wormCoords, wormcolor, direction, cyanHead)
        elif wormcolor == PURPLE:
            drawWorm(wormCoords, wormcolor, direction, purpleHead)
        elif wormcolor == PINK:
            drawWorm(wormCoords, wormcolor, direction, pinkHead)
        
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

    congratFont = pygame.font.Font('freesansbold.ttf', 70)
    congratSurf = congratFont.render('Congratulations!', True, WHITE)
    congratRect = congratSurf.get_rect()
    congratRect.midtop = (WINDOWWIDTH/2, 80)

    highFont = pygame.font.Font('freesansbold.ttf', 55)
    highSurf = highFont.render('New Highest Score!', True, WHITE)
    highRect = highSurf.get_rect()
    highRect.midtop = (WINDOWWIDTH/2, congratRect.height+110)

    returnFont = pygame.font.Font('freesansbold.ttf', 18)
    returnSurf = returnFont.render('Press any button to restart', True, WHITE)
    returnRect = returnSurf.get_rect()
    returnRect.midbottom = (WINDOWWIDTH/2, 470)

    highestFont = pygame.font.Font('freesansbold.ttf', 25)
    highestSurf = highestFont.render('Your highest (Single Player) is: ' + str(HIGHEST), True, WHITE)
    highestRect = highestSurf.get_rect()
    highestRect.midbottom = (WINDOWWIDTH/2, 400)

    mainFont = pygame.font.Font('freesansbold.ttf', 18)
    mainSurf = mainFont.render('Press "RETURN" to go back to main page', True, WHITE)
    mainRect = mainSurf.get_rect()
    mainRect.midbottom = (WINDOWWIDTH/2, 440)

    gameFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameFont.render('Game', True, WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2, 35)

    overFont = pygame.font.Font('freesansbold.ttf', 150)
    overSurf = overFont.render('Over', True, WHITE)
    overRect = overSurf.get_rect()
    overRect.midtop = (WINDOWWIDTH/2, gameRect.height+50)
    
    if IFHIGHEST:
        pygame.mixer.Sound.play(win)
        DISPLAYSURF.blit(congratSurf, congratRect)
        DISPLAYSURF.blit(highSurf, highRect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(highestSurf, highestRect)
        DISPLAYSURF.blit(mainSurf, mainRect)
    else:
        pygame.mixer.Sound.play(fail)
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(highestSurf, highestRect)
        DISPLAYSURF.blit(mainSurf, mainRect)

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # Clear the event cache

    while True:
        if checkForKeyPress() == 'Restart':
            pygame.mixer.Sound.play(SELECT)
            pygame.event.get()
            return 'Restart'
        elif checkForKeyPress() == 'Main':
            pygame.mixer.Sound.play(SELECT)
            pygame.event.get()
            return 'Main'

def updateHighest(score):
    if score > HIGHEST:
        return score, True
    else:
        return HIGHEST, False

def drawWorm(wormCoords, wormcolor, direction, image):
    x = wormCoords[0]['x'] * CELLSIZE
    y = wormCoords[0]['y'] * CELLSIZE
    if direction == UP:
        wormHeadImage = pygame.transform.rotate(image, 180)
    elif direction == DOWN:
        wormHeadImage = image
    elif direction == LEFT:
        wormHeadImage = pygame.transform.rotate(image, 270)
    elif direction == RIGHT:
        wormHeadImage = pygame.transform.rotate(image, 90)
    wormHeadRect = wormHeadImage.get_rect()
    wormHeadRect.top = y
    wormHeadRect.left = x
    DISPLAYSURF.blit(wormHeadImage, wormHeadRect)

    for segment in wormCoords[1:]:
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

def drawGrid():
    for x in range(0, WINDOWWIDTH-1, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0), (x,WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT-1, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH,y))

# ==========Double Player Functions==========

def DchangeColorP1():
    DISPLAYSURF.fill(BGCOLOR)

    setColorFont = pygame.font.Font('freesansbold.ttf', 90)
    setColorSurf = setColorFont.render('P1: Press any number', True, WHITE)
    setColorRect = setColorSurf.get_rect()
    setColorRect.midtop = (WINDOWWIDTHD/2, 50)

    setColorSurf2 = setColorFont.render('to set your worm\'s color', True, WHITE)
    setColorRect2 = setColorSurf2.get_rect()
    setColorRect2.midtop = (WINDOWWIDTHD/2, 170)

    DISPLAYSURF.blit(setColorSurf, setColorRect)
    DISPLAYSURF.blit(setColorSurf2, setColorRect2)

    Surf0 = setColorFont.render('0', True, WHITE)
    Rect0 = Surf0.get_rect()
    Rect0.midtop = (214, 353)
    DISPLAYSURF.blit(Surf0, Rect0)

    Surf1 = setColorFont.render('1', True, RED)
    Rect1 = Surf1.get_rect()
    Rect1.midtop = (427, 353)
    DISPLAYSURF.blit(Surf1, Rect1)

    Surf2 = setColorFont.render('2', True, GREEN)
    Rect2 = Surf2.get_rect()
    Rect2.midtop = (WINDOWWIDTHD/2, 353)
    DISPLAYSURF.blit(Surf2, Rect2)

    Surf3 = setColorFont.render('3', True, DARKGREEN)
    Rect3 = Surf3.get_rect()
    Rect3.midtop = (853, 353)
    DISPLAYSURF.blit(Surf3, Rect3)

    Surf4 = setColorFont.render('4', True, DARKGRAY)
    Rect4 = Surf4.get_rect()
    Rect4.midtop = (1066, 353)
    DISPLAYSURF.blit(Surf4, Rect4)

    Surf5 = setColorFont.render('5', True, BLUE)
    Rect5 = Surf5.get_rect()
    Rect5.topleft = (214, 576)
    DISPLAYSURF.blit(Surf5, Rect5)

    Surf6 = setColorFont.render('6', True, YELLOW)
    Rect6 = Surf6.get_rect()
    Rect6.midtop = (427, 576)
    DISPLAYSURF.blit(Surf6, Rect6)

    Surf7 = setColorFont.render('7', True, CYAN)
    Rect7 = Surf7.get_rect()
    Rect7.midtop = (WINDOWWIDTHD/2, 576)
    DISPLAYSURF.blit(Surf7, Rect7)

    Surf8 = setColorFont.render('8', True, PURPLE)
    Rect8 = Surf8.get_rect()
    Rect8.midtop = (853, 576)
    DISPLAYSURF.blit(Surf8, Rect8)

    Surf9 = setColorFont.render('9', True, PINK)
    Rect9 = Surf9.get_rect()
    Rect9.midtop = (1066, 576)
    DISPLAYSURF.blit(Surf9, Rect9)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                pygame.mixer.Sound.play(SELECT)
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

def DchangeColorP2():
    DISPLAYSURF.fill(BGCOLOR)

    setColorFont = pygame.font.Font('freesansbold.ttf', 90)
    setColorSurf = setColorFont.render('P2: Press any number', True, WHITE)
    setColorRect = setColorSurf.get_rect()
    setColorRect.midtop = (WINDOWWIDTHD/2, 50)

    setColorSurf2 = setColorFont.render('to set your worm\'s color', True, WHITE)
    setColorRect2 = setColorSurf2.get_rect()
    setColorRect2.midtop = (WINDOWWIDTHD/2, 170)

    DISPLAYSURF.blit(setColorSurf, setColorRect)
    DISPLAYSURF.blit(setColorSurf2, setColorRect2)

    Surf0 = setColorFont.render('0', True, WHITE)
    Rect0 = Surf0.get_rect()
    Rect0.midtop = (214, 353)
    DISPLAYSURF.blit(Surf0, Rect0)

    Surf1 = setColorFont.render('1', True, RED)
    Rect1 = Surf1.get_rect()
    Rect1.midtop = (427, 353)
    DISPLAYSURF.blit(Surf1, Rect1)

    Surf2 = setColorFont.render('2', True, GREEN)
    Rect2 = Surf2.get_rect()
    Rect2.midtop = (WINDOWWIDTHD/2, 353)
    DISPLAYSURF.blit(Surf2, Rect2)

    Surf3 = setColorFont.render('3', True, DARKGREEN)
    Rect3 = Surf3.get_rect()
    Rect3.midtop = (853, 353)
    DISPLAYSURF.blit(Surf3, Rect3)

    Surf4 = setColorFont.render('4', True, DARKGRAY)
    Rect4 = Surf4.get_rect()
    Rect4.midtop = (1066, 353)
    DISPLAYSURF.blit(Surf4, Rect4)

    Surf5 = setColorFont.render('5', True, BLUE)
    Rect5 = Surf5.get_rect()
    Rect5.topleft = (214, 576)
    DISPLAYSURF.blit(Surf5, Rect5)

    Surf6 = setColorFont.render('6', True, YELLOW)
    Rect6 = Surf6.get_rect()
    Rect6.midtop = (427, 576)
    DISPLAYSURF.blit(Surf6, Rect6)

    Surf7 = setColorFont.render('7', True, CYAN)
    Rect7 = Surf7.get_rect()
    Rect7.midtop = (WINDOWWIDTHD/2, 576)
    DISPLAYSURF.blit(Surf7, Rect7)

    Surf8 = setColorFont.render('8', True, PURPLE)
    Rect8 = Surf8.get_rect()
    Rect8.midtop = (853, 576)
    DISPLAYSURF.blit(Surf8, Rect8)

    Surf9 = setColorFont.render('9', True, PINK)
    Rect9 = Surf9.get_rect()
    Rect9.midtop = (1066, 576)
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

def DrunGame(wormcolor1, wormcolor2):

    # Set Up Game
    fpsD = 10
    wormP1 = Worms(random.randint(5, CELLWIDTHD/2-5), random.randint(5, CELLHEIGHTD-5), RIGHT, 0, 4, wormcolor1)
    wormP2 = Worms(random.randint(CELLWIDTHD/2-5, CELLWIDTH-5), random.randint(5, CELLHEIGHTD-5), RIGHT, 0, 4, wormcolor2)
    wormP1startx = wormP1.startx
    wormP1starty = wormP1.starty
    wormP2startx = wormP2.startx
    wormP2starty = wormP2.starty
    wormCoordsP1 = [{'x': wormP1startx, 'y': wormP1starty},
                    {'x': wormP1startx - 1, 'y': wormP1starty},
                    {'x': wormP1startx - 2, 'y': wormP1starty}]
    wormCoordsP2 = [{'x': wormP2startx, 'y': wormP2starty},
                    {'x': wormP2startx-1, 'y': wormP2starty},
                    {'x': wormP2startx-2, 'y': wormP2starty}]
    appleList = []
    for i in range(6):
        i = DgetRandomLocation()
        appleList.append(i)

    P1ateApple = False
    P2ateApple = False
    P1Faster = False
    P1Slower = False
    P2Faster = False
    P2Slower = False

    whiteHead = pygame.image.load('1White.png')
    redHead = pygame.image.load('2Red.png')
    greenHead = pygame.image.load('3Green.png')
    darkGreenHead = pygame.image.load('4Dark_green.png')
    darkGrayHead = pygame.image.load('5Dark_gray.png')
    blueHead = pygame.image.load('6Blue.png')
    yellowHead = pygame.image.load('7Yellow.png')
    cyanHead = pygame.image.load('8Cyan.png')
    purpleHead = pygame.image.load('9Purple.png')
    pinkHead = pygame.image.load('10Pink.png')

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
                pygame.mixer.Sound.play(turn)
                if (event.key == K_LEFT) and wormP1.direction != RIGHT:
                    wormP1.direction = LEFT
                elif (event.key == K_RIGHT) and wormP1.direction != LEFT:
                    wormP1.direction = RIGHT
                elif (event.key == K_UP) and wormP1.direction != DOWN:
                    wormP1.direction = UP
                elif (event.key == K_DOWN) and wormP1.direction != UP:
                    wormP1.direction = DOWN
                elif(event.key == K_a) and wormP2.direction != RIGHT:
                    wormP2.direction = LEFT
                elif(event.key == K_d) and wormP2.direction != LEFT:
                    wormP2.direction = RIGHT
                elif(event.key == K_w) and wormP2.direction != DOWN:
                    wormP2.direction = UP
                elif(event.key == K_s) and wormP2.direction != UP:
                    wormP2.direction = DOWN
                elif (event.key == K_ESCAPE):
                    terminate()

        # Detect P1 "Collisions" With Wall
        if wormCoordsP1[HEAD]['x'] <= -1 or wormCoordsP1[HEAD]['y'] <= -1 or wormCoordsP1[HEAD]['x'] >= CELLWIDTHD or wormCoordsP1[HEAD]['y'] >= CELLHEIGHTD:
            return "P1Died"
        # Detect P2 "Collisions" With Wall
        if wormCoordsP2[HEAD]['x'] <= -1 or wormCoordsP2[HEAD]['y'] <= -1 or wormCoordsP2[HEAD]['x'] >= CELLWIDTHD or wormCoordsP2[HEAD]['y'] >= CELLHEIGHTD:
            return "P2Died"

        # Detect P1 "Collisions" with self Body
        for wormSegment in wormCoordsP1[3:]:
            if wormSegment['x'] == wormCoordsP1[HEAD]['x'] and wormSegment['y'] == wormCoordsP1[HEAD]['y']:
                return "P1Died"
        # Detect P2 "Collisions" with self Body
        for wormSegment in wormCoordsP2[3:]:
            if wormSegment['x'] == wormCoordsP2[HEAD]['x'] and wormSegment['y'] == wormCoordsP2[HEAD]['y']:
                return "P2Died"

        # Detect P1 and P2 "Collisions" with each other
        for wormSegment in wormCoordsP1[0:]:
            if wormSegment['x'] == wormCoordsP2[HEAD]['x'] and wormSegment['y'] == wormCoordsP2[HEAD]['y']:
                return "P2Died"
        for wormSegment in wormCoordsP2[0:]:
            if wormSegment['x'] == wormCoordsP1[HEAD]['x'] and wormSegment['y'] == wormCoordsP1[HEAD]['y']:
                return "P1Died"
        if wormCoordsP1[HEAD]['x'] == wormCoordsP2[HEAD]['x'] and wormCoordsP1[HEAD]['y'] == wormCoordsP2[HEAD]['y']:
            return "Tied"

        # Detect P1 "Collisions" With Apple
        for i in range(len(appleList)):
            if wormCoordsP1[HEAD]['x'] == appleList[i].x and wormCoordsP1[HEAD]['y'] == appleList[i].y:
                P1ateApple = True
                if appleList[i].ability == 'faster' and wormP1.speed < 7:
                    P1Faster = True
                elif appleList[i].ability == 'slower' and wormP1.speed > 2:
                    P1Slower = True
                else:
                    fpsD += 0
                appleList[i] = DgetRandomLocation()

        # Detect P2 "Collisions" With Apple
        for i in range(len(appleList)):
            if wormCoordsP2[HEAD]['x'] == appleList[i].x and wormCoordsP2[HEAD]['y'] == appleList[i].y:
                P2ateApple = True
                if appleList[i].ability == 'faster' and wormP2.speed < 7:
                    P2Faster = True
                elif appleList[i].ability == 'slower' and wormP2.speed > 2:
                    P2Slower = True
                else:
                    fpsD += 0
                appleList[i] = DgetRandomLocation()

        if P1ateApple == True:
            pygame.mixer.Sound.play(eatSound[random.randint(0,1)])
            if P1Faster == True:
                fpsD += 3
                wormP1.speed += 1
                wormP2.speed += 1
                P1Faster = False
            if P1Slower == True:
                fpsD -= 3
                wormP1.speed -= 1
                wormP2.speed -= 1
                P1Slower = False
            P1ateApple = False
        else:
            del wormCoordsP1[-1]

        if P2ateApple == False:
            del wormCoordsP2[-1]
        else:
            pygame.mixer.Sound.play(eatSound[random.randint(0,1)])
            if P2Faster == True:
                fpsD += 3
                wormP1.speed += 1
                wormP2.speed += 1
                P2Faster = False
            if P2Slower == True:
                fpsD -= 3
                wormP1.speed -= 1
                wormP2.speed -= 1
                P2Slower = False
            P2ateApple = False
        
        # Move The P1 Worm
        if wormP1.direction == UP:
           newHeadP1 = {'x': wormCoordsP1[HEAD]['x'], 'y': wormCoordsP1[HEAD]['y']-1}
        elif wormP1.direction == DOWN:
            newHeadP1 = {'x': wormCoordsP1[HEAD]['x'], 'y': wormCoordsP1[HEAD]['y']+1}
        elif wormP1.direction == LEFT:
            newHeadP1 = {'x': wormCoordsP1[HEAD]['x']-1, 'y': wormCoordsP1[HEAD]['y']}
        elif wormP1.direction == RIGHT:
            newHeadP1 = {'x': wormCoordsP1[HEAD]['x']+1, 'y': wormCoordsP1[HEAD]['y']}
        # Move The P2 Worm
        if wormP2.direction == UP:
            newHeadP2 = {'x': wormCoordsP2[HEAD]['x'], 'y': wormCoordsP2[HEAD]['y']-1}
        elif wormP2.direction == DOWN:
            newHeadP2 = {'x': wormCoordsP2[HEAD]['x'], 'y': wormCoordsP2[HEAD]['y']+1}
        elif wormP2.direction == LEFT:
            newHeadP2 = {'x': wormCoordsP2[HEAD]['x']-1, 'y': wormCoordsP2[HEAD]['y']}
        elif wormP2.direction == RIGHT:
            newHeadP2 = {'x': wormCoordsP2[HEAD]['x']+1, 'y': wormCoordsP2[HEAD]['y']}

        wormCoordsP1.insert(0, newHeadP1)
        wormCoordsP2.insert(0, newHeadP2)

        # Paint On The Screen
        DISPLAYSURF.fill(BGCOLOR)
        DdrawGrid()

        if wormP1.color == WHITE:
            DdrawWorm(wormCoordsP1, wormP1, whiteHead)
        elif wormP1.color == RED:
            DdrawWorm(wormCoordsP1, wormP1, redHead)
        elif wormP1.color == GREEN:
            DdrawWorm(wormCoordsP1, wormP1, greenHead)
        elif wormP1.color == DARKGREEN:
            DdrawWorm(wormCoordsP1, wormP1, darkGreenHead)
        elif wormP1.color == DARKGRAY:
            DdrawWorm(wormCoordsP1, wormP1, darkGrayHead)
        elif wormP1.color == BLUE:
            DdrawWorm(wormCoordsP1, wormP1, blueHead)
        elif wormP1.color == YELLOW:
            DdrawWorm(wormCoordsP1, wormP1, yellowHead)
        elif wormP1.color == CYAN:
            DdrawWorm(wormCoordsP1, wormP1, cyanHead)
        elif wormP1.color == PURPLE:
            DdrawWorm(wormCoordsP1, wormP1, purpleHead)
        elif wormP1.color == PINK:
            DdrawWorm(wormCoordsP1, wormP1, pinkHead)

        if wormP2.color == WHITE:
            DdrawWorm(wormCoordsP2, wormP2, whiteHead)
        elif wormP2.color == RED:
            DdrawWorm(wormCoordsP2, wormP2, redHead)
        elif wormP2.color == GREEN:
            DdrawWorm(wormCoordsP2, wormP2, greenHead)
        elif wormP2.color == DARKGREEN:
            DdrawWorm(wormCoordsP2, wormP2, darkGreenHead)
        elif wormP2.color == DARKGRAY:
            DdrawWorm(wormCoordsP2, wormP2, darkGrayHead)
        elif wormP2.color == BLUE:
            DdrawWorm(wormCoordsP2, wormP2, blueHead)
        elif wormP2.color == YELLOW:
            DdrawWorm(wormCoordsP2, wormP2, yellowHead)
        elif wormP2.color == CYAN:
            DdrawWorm(wormCoordsP2, wormP2, cyanHead)
        elif wormP2.color == PURPLE:
            DdrawWorm(wormCoordsP2, wormP2, purpleHead)
        elif wormP2.color == PINK:
            DdrawWorm(wormCoordsP2, wormP2, pinkHead)
        
        DdrawApple(appleList)
        DdrawSpeed(wormP1.speed, 5, 'P1')
        DdrawSpeed(wormP2.speed, 1170, 'P2')
        pygame.display.update()
        FPSCLOCK.tick(fpsD)

def DshowGameOverScreen(reason):
    DISPLAYSURF.fill(BGCOLOR)

    # Sounds
    win = pygame.mixer.Sound('Win.wav')

    congratFont = pygame.font.Font('freesansbold.ttf', 70)
    congratSurf = congratFont.render('Congratulations!', True, WHITE)
    congratRect = congratSurf.get_rect()
    congratRect.midtop = (WINDOWWIDTHD/2, 80)

    p1Font = pygame.font.Font('freesansbold.ttf', 55)
    p1Surf = p1Font.render('Player 1 Won!', True, WHITE)
    p1Rect = p1Surf.get_rect()
    p1Rect.midtop = (WINDOWWIDTHD/2, congratRect.height+180)

    p2Font = pygame.font.Font('freesansbold.ttf', 150)
    p2Surf = p2Font.render('Player 2 Won!', True, WHITE)
    p2Rect = p2Surf.get_rect()
    p2Rect.midtop = (WINDOWWIDTHD/2, congratRect.height+180)

    tiedFont = pygame.font.Font('freesansbold.ttf', 150)
    tiedSurf = tiedFont.render('Tied!', True, WHITE)
    tiedRect = tiedSurf.get_rect()
    tiedRect.midtop = (WINDOWWIDTHD/2, congratRect.height+180)

    mainFont = pygame.font.Font('freesansbold.ttf', 30)
    mainSurf = mainFont.render('Press "RETURN" to go back to main page', True, WHITE)
    mainRect = mainSurf.get_rect()
    mainRect.midbottom = (WINDOWWIDTHD/2, WINDOWHEIGHTD-100)

    returnFont = pygame.font.Font('freesansbold.ttf', 30)
    returnSurf = returnFont.render('Press any button to restart', True, WHITE)
    returnRect = returnSurf.get_rect()
    returnRect.midbottom = (WINDOWWIDTHD/2, WINDOWHEIGHTD-40)
    
    if reason == "P1Died":
        pygame.mixer.Sound.play(win)
        DISPLAYSURF.blit(congratSurf, congratRect)
        DISPLAYSURF.blit(p2Surf, p2Rect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(mainSurf, mainRect)
    elif reason == "P2Died":
        pygame.mixer.Sound.play(win)
        DISPLAYSURF.blit(congratSurf, congratRect)
        DISPLAYSURF.blit(p1Surf, p1Rect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(mainSurf, mainRect)
    else:
        pygame.mixer.Sound.play(win)
        DISPLAYSURF.blit(congratSurf, congratRect)
        DISPLAYSURF.blit(tiedSurf, tiedRect)
        DISPLAYSURF.blit(returnSurf, returnRect)
        DISPLAYSURF.blit(mainSurf, mainRect)

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # Clear the event cache

    while True:
        if checkForKeyPress() == 'Restart':
            pygame.mixer.Sound.play(SELECT)
            pygame.event.get()
            return 'Restart'
        elif checkForKeyPress() == 'Main':
            pygame.mixer.Sound.play(SELECT)
            pygame.event.get()
            return 'Main'
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
def DdrawWorm(wormCoords, worm, image):
    x = wormCoords[0]['x'] * CELLSIZE
    y = wormCoords[0]['y'] * CELLSIZE
    if worm.direction == UP:
        wormHeadImage = pygame.transform.rotate(image, 180)
    elif worm.direction == DOWN:
        wormHeadImage = image
    elif worm.direction == LEFT:
        wormHeadImage = pygame.transform.rotate(image, 270)
    elif worm.direction == RIGHT:
        wormHeadImage = pygame.transform.rotate(image, 90)
    
    wormHeadRect = wormHeadImage.get_rect()
    wormHeadRect.top = y
    wormHeadRect.left = x
    DISPLAYSURF.blit(wormHeadImage, wormHeadRect)
    for segment in wormCoords[1:]:
        x = segment['x'] * CELLSIZE
        y = segment['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, worm.color, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)

def DdrawApple(appleList):
    for i in appleList:
        x = i.x * CELLSIZE
        y = i.y * CELLSIZE
        appleSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, i.color, appleSegmentRect)

def DdrawSpeed(speed, horizontalPos, player):
    speedFont = pygame.font.Font('freesansbold.ttf', 18)
    speedSurf = speedFont.render(player+' Speed: '+str(speed), True, WHITE)
    speedRect = speedSurf.get_rect()
    speedRect.top = (5)
    speedRect.left = (horizontalPos)
    DISPLAYSURF.blit(speedSurf, speedRect)
    return

def DgetRandomLocation():
    all_abilities = ['faster', 'slower', 'none', 'none', 'none', 'none']
    randAbility = all_abilities[random.randint(0,len(all_abilities)-1)]
    color = None
    if randAbility == 'faster':
        color = GREEN
    elif randAbility == 'slower':
        color = YELLOW
    else:
        color = RED
    apple = Apples(random.randint(0, CELLWIDTHD-1), random.randint(0, CELLHEIGHTD-1), randAbility, color)
    return apple

def DcountDown():
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
            countDownRect.center = (WINDOWWIDTHD/2, WINDOWHEIGHTD/2)
            DISPLAYSURF.blit(countDownSurf, countDownRect)
            pygame.display.update()
            FPSCLOCK.tick(2)
        return

def DdrawGrid():
    for x in range(0, WINDOWWIDTHD-1, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0), (x,WINDOWHEIGHTD))
    for y in range(0, WINDOWHEIGHTD-1, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTHD,y))

# ==========Other Functions==========

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

#add a picture to the head of the snake
#double player mode