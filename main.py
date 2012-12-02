from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pygame
import math
import random
import time
import inputbox
from pygame.locals import *

pygame.init()

# Constants:
FPS = 60                # frames per second setting
GRAVITY = 7           # The speed at which the character falls
MOVEMENT_SPEED = 25    # The speed at which the char moves left or right.
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BASELINE = 500     # The "floor" which the character can go no lower than.
CHAR_SPRITE = 'cat.png' # The sprite for the player character
SCREEN_WIDTH   = 800
SCREEN_HEIGHT  = 600
PLATFORM_HEIGHT = 70
PLATFORM_WIDTH = 150
MAX_FLOOR = 0
Y_DISTANCE_BETWEEN_PLATFORMS = 300
INITIAL_PLATFORM_HEIGHT = 300
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                      DOUBLEBUF|HWSURFACE)
FONT = pygame.font.SysFont('Helvetica', 20)
FINAL_TIME = 0
SCROLL = 900
LAVA_SPEED = 1

INITIAL_LAVA = 120


fpsClock = pygame.time.Clock()
thePlatform = pygame.Rect(150, 300, 150, 50)
platforms = []

noOfQuestions = 0
speed = 0    

class Character:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.jump = False
        self.verticalSpeed = 0
        self.horizontalSpeed = 0
        self.img = pygame.image.load("player.png")
        self.falling = False
        self.onAPlatform = False

    def onPlatform(self, platforms, bottomOfChar, middleOfChar):
        for i in platforms:
            if bottomOfChar + 1 > i.y1 and bottomOfChar + 1 < i.y2 \
                          and self.x + 56 > i.x1 and self.x  < i.x2:
                return i
        return False

    def draw(self):
        global platforms
        global FINAL_TIME
        bottomOfChar = self.y + 115
        middleOfChar = self.x + 28

        # Handle horizontal movement
        if self.x >= 10 and self.x <= 660:
            self.x += self.horizontalSpeed
            middleOfChar += self.horizontalSpeed
        if self.x < 10:
            self.x = 10
            middleOfChar = 89 - 28
        elif self.x > 660:
            self.x = 660
            middleOfChar = 660 + 79 - 28

        #if self.onPlatform(platforms, bottomOfChar - 20,
        #                           middleOfChar) != False:
        #    print("platform")
        #else:
        #    print( self.verticalSpeed )
        #    print( self.jump )

        #if self.onPlatform(platforms, bottomOfChar - 20, middleOfChar) != False:
         #   print("ok")
        
        if self.jump:
            pass
        elif self.y == BASELINE:
            self.falling = False
            self.verticalSpeed = 0
        elif self.onPlatform(platforms, bottomOfChar, middleOfChar) != False and self.verticalSpeed < 1 :
            platform = self.onPlatform(platforms, bottomOfChar, middleOfChar)
            if platform.right == True:
                self.falling = False
                self.onAPlatform = True
                self.verticalSpeed = 0
                self.y = platform.y1 - 115
        elif self.onPlatform(platforms, bottomOfChar, middleOfChar) == False and self.verticalSpeed < 1 and self.y != BASELINE:
            self.falling = True
            self.onAPlatform = False

        


        if self.falling:
            self.jump = False
            # Move up or down according to speed.
            self.y -= self.verticalSpeed
            bottomOfChar -= self.verticalSpeed

            # Check to see if on baseline:
            if self.y > BASELINE:
                self.y = BASELINE
                self.falling = False
                self.verticalSpeed = 0
            # If not on baseline, check if on a platform:
            else:
                platform = self.onPlatform(platforms, bottomOfChar,
                                               middleOfChar)
               
                if platform != False and self.verticalSpeed < 1:
                    if platform.right == True:
                        platforms[platform.floor*3].right = True
                        platforms[platform.floor*3+1].right = True
                        platforms[platform.floor*3+2].right = True
                        self.y = platform.y1 - 115
                        self.falling = False
                        self.verticalSpeed = 0
                        self.onAPlatform = True
                        if MAX_FLOOR - 1 == platform.floor:
                            FINAL_TIME = time.time()
            
            if self.falling:
                self.verticalSpeed -= GRAVITY

        
        if self.x < 10:
            self.x = 10
        elif self.x > 660:
            self.x = 660
        DISPLAYSURF.blit(self.img, (self.x, self.y))

    def offset(self):
        if self.y < 200:
            temp = 200 - self.y
            self.y = 200
            return temp
        elif self.y > 500:
            temp = 500 - self.y 
            self.y = 500
            return temp
        else:
            return 0
        
class Platform:

    # Pass the constructor the co-ordinates of the top-left corner
    def __init__(self, x, y, answer, right, floor):
        self.floor = floor
        self.right = right
        self.x1 = x                   # The left boundary
        self.x2 = x + PLATFORM_WIDTH  # The right boundary
        self.y1 = y                   # The top boundary
        self.y2 = y + PLATFORM_HEIGHT # The bottom boundary
        self.answer = answer
        self.img = pygame.image.load("platform.png")
        
    def draw(self, offset):
        self.y1 = self.y1 + offset
        self.y2 = self.y2 + offset
        if self.y1 > -20 and self.y1 < 800:
            DISPLAYSURF.blit(self.img, (self.x1, (int)(self.y1)))
            printText(self.answer, self.x1 + 75, self.y1 - 25 )

class Lava:
    def __init__( self):
        self.x = 0
        self.y = SCREEN_HEIGHT + INITIAL_LAVA
        self.img = pygame.image.load("lava.png")

    def draw(self, char, offset ):
        self.y -= ( LAVA_SPEED - offset )
        DISPLAYSURF.blit(self.img, (self.x, (int)(self.y)))
        if( self.y < char.y ):
            return True
        else:
            return False
lava = Lava()

class Question:
    def __init__(self, x, y, question):
        self.x = x
        self.y = y
        self.question = question

    def draw(self, offset):
        self.y = self.y + offset
        if self.y > -20 and self.y < 800:
            printCenterText( self.question, self.x, self.y)

class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("background.png")

    def draw(self, offset):
        self.y = self.y + offset
        DISPLAYSURF.blit(self.img, (self.x, (int)(self.y)))

            
def printText(txtText, Textx, Texty):
      # apply it to text on a label
      label = FONT.render(txtText, 1, (255,255,255))
      # put the label object on the screen at point Textx, Texty
      DISPLAYSURF.blit(label, (Textx, Texty))

def printCenterText(txtText, Textx, Texty):
      # apply it to text on a label
      label = FONT.render(txtText, 1, (150,150,255))
      tempPos = label.get_rect()
      Textx = SCREEN_WIDTH / 2 + tempPos.right - tempPos.left
      # put the label object on the screen at point Textx, Texty
      DISPLAYSURF.blit(label, (Textx, Texty))

def leader_board( result ):
    leaderBoardFile = open("leader_board.txt", "r+")
    leaderBoard = []
    i = 1
    while True:
        text = leaderBoardFile.readline()
        if not text:
            break
        leaderBoard.append(text.split('\t')[0])
        leaderBoard.append(text.split('\t')[1])
        leaderBoard[i] = leaderBoard[i][:-1]
        i += 2
    leaderBoardFile.close()
    leaderBoardFile = open("leader_board.txt", "r+")
    if result != -1 and len(leaderBoard) == 10 and result < leaderBoard[len(leaderBoard)-1]:
        name = inputbox.ask(DISPLAYSURF, "Type a pseudo" )
        print( leaderBoard)
        i = len(leaderBoard) - 1
        while i > 0 and result < (int)(leaderBoard[i]):
            i -= 2
        i += 2
        print(i)
        print( leaderBoard)
        for j in  range(len(leaderBoard)-1, i, -1 ):
            leaderBoard[j] = leaderBoard[j-2]
        print( leaderBoard)
        leaderBoard[i] = result
        leaderBoard[i-1] = name
        print( leaderBoard)
        for j in  range(0, len(leaderBoard)-1, 2 ):
            leaderBoardFile.write('%s\t%s\n' % (leaderBoard[j], leaderBoard[j+1]))
        leaderBoardFile.close()
    elif len(leaderBoard) == 0:
        name = inputbox.ask(DISPLAYSURF, "Type a pseudo" )
        leaderBoard.append(name)
        leaderBoard.append(str(result))
        for j in  range(0, len(leaderBoard)-1, 2 ):
            leaderBoardFile.write('%s\t%s' % (leaderBoard[j], leaderBoard[j+1]))
    elif len(leaderBoard) < 10:
        name = inputbox.ask(DISPLAYSURF, "Type a pseudo" )
        print( leaderBoard)
        i = len(leaderBoard) - 1
        while i > 0 and result < (int)(leaderBoard[i]):
            i -= 2
        i += 2
        print(i)
        leaderBoard.append(0)
        leaderBoard.append(0)
        print( leaderBoard)
        for j in  range(len(leaderBoard)-1, i, -1 ):
            leaderBoard[j] = leaderBoard[j-2]
        print( leaderBoard)
        leaderBoard[i] = result
        leaderBoard[i-1] = name
        print( leaderBoard)
        for j in  range(0, len(leaderBoard)-1, 2 ):
            leaderBoardFile.write('%s\t%s\n' % (leaderBoard[j], leaderBoard[j+1]))
        leaderBoardFile.close()
    done = True
    while done:
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():    
            if event.type == QUIT:
                done = False
                return True
        for i in range(0, len(leaderBoard)-1, 2 ):
            printCenterText( ''.join('%s\t%s' % (leaderBoard[i], str(leaderBoard[i+1]))), 0, 10+i*20)
        pygame.display.flip()

        

    


    
def play( field):
    print(field)
    stop = False
    global platforms
    global MAX_FLOOR
    global lava
    start_time = (int)(time.time())
    global BASELINE

    objs = []
    
    # Code that creates a file called questions.txt
    execfile("QuestionGenerator.py")

    # Reads the questions from the text file and stores in questions_file
    questionsFile = open(field, 'r')
    # questions contains the questions, correct answers and options
    questions = []
    while 1 :
        newQuestions = questionsFile.readline()
        if not newQuestions:
            break
        newQuestions = newQuestions[0:-1]

        questions = questions + newQuestions.split( '\t' )

    assert len(questions) % 5 == 0 # Sanity check
    
    noOfQuestions = len(questions) // 5

    background = Background(0, -5400)  

    list_answers = []
    platforms = []

    MAX_FLOOR = noOfQuestions
    for i in range(0, noOfQuestions):
        #if( questions[i*5+2] == questions[i*5] or questions[i*5+3] == questions[i*5] or questions[i*5+4] == questions[i*5] )
         #   print("ok")
        platforms.append( Platform( 75,
                              -i * Y_DISTANCE_BETWEEN_PLATFORMS +
                              INITIAL_PLATFORM_HEIGHT,
                              questions[i*5+2],
                              questions[i*5+2] == questions[i*5+1],
                              i))
        platforms.append( Platform( 325,
                              -i * Y_DISTANCE_BETWEEN_PLATFORMS +
                              INITIAL_PLATFORM_HEIGHT,
                              questions[i*5+3],
                              questions[i*5+3] == questions[i*5+1],
                              i))
        platforms.append( Platform( 575,
                              -i * Y_DISTANCE_BETWEEN_PLATFORMS +
                              INITIAL_PLATFORM_HEIGHT,
                              questions[i*5+4],
                              questions[i*5+4] == questions[i*5+1],
                              i))
        list_answers.append( questions[i*5+1] )
        objs.append(Question(0,
                                -i * Y_DISTANCE_BETWEEN_PLATFORMS +
                                INITIAL_PLATFORM_HEIGHT + PLATFORM_HEIGHT,
                                questions[i*5]) )

    lava = Lava()
    # Remember if the left arrow or right arrow are currently held down.
    # Without these variables, if you lift one key while the other key is 
    # already held down, the character will stop moving, instead of the
    # desired behaviour which is to move in the opposite direction.
    leftKeyPressed  = False
    rightKeyPressed = False

    # Create the display DISPLAYSURF:
    pygame.display.set_caption("Jump!")
    pygame.mouse.set_visible(0)

    # Load the player character:
    theChar = Character(260, BASELINE, CHAR_SPRITE)

    done = False
    while not done and not stop:
        DISPLAYSURF.fill(WHITE)
        


        for event in pygame.event.get():
            # If a key is pressed down...
            if event.type == KEYDOWN:
                # If the left arrow is pressed, change the speed of the 
                # character
                if event.key == K_LEFT:
                    leftKeyPressed = True
                    # Only change the speed if the character is not 
                    # already moving. (In practice, he can only be moving
                    # in the opposite direction)
                    if theChar.horizontalSpeed == 0:
                        theChar.horizontalSpeed -= MOVEMENT_SPEED
                # Similarly if the right arrow is pressed:
                if event.key == K_RIGHT:
                    rightKeyPressed = True
                    if theChar.horizontalSpeed == 0:
                        theChar.horizontalSpeed += MOVEMENT_SPEED
                # Space to jump
                if event.key == K_SPACE:
                    if theChar.falling == False:
                        theChar.verticalSpeed = 70 
                        theChar.falling = True
                        theChar.jump = True
                if (event.key == K_ESCAPE):
                    return True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    leftKeyPressed = False
                    theChar.horizontalSpeed = 0
                    if rightKeyPressed:
                        theChar.horizontalSpeed += MOVEMENT_SPEED
                if event.key == K_RIGHT:
                    rightKeyPressed = False
                    theChar.horizontalSpeed = 0
                    if leftKeyPressed:
                        theChar.horizontalSpeed -= MOVEMENT_SPEED
            if event.type == QUIT:
                done = True
                return False


        # Compute an offset and update all the positions of the platforms:
        offset = theChar.offset()
        background.draw(offset)
        for i in objs:
            i.draw(offset)
        for i in platforms:
            i.draw(offset)
        BASELINE = BASELINE + offset

        # Draw the character
        theChar.draw()

        

        test = lava.draw(theChar, offset)
        if test == True:
            return True

        # Display the time elapsed since the start of the game:
        printText( str((int)( time.time() - start_time ) ), 0, 0)

        
        pygame.display.flip()
        fpsClock.tick(FPS)

        if FINAL_TIME != 0:
            done = True
            
    return leader_board((int)( time.time() - start_time ) )
        
    

class Box:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))
        
def startMenu():
    pygame.mouse.set_visible(1)
    done = True
    boxes = [ Box( 250, 300, "maths.png") ]
    boxes.append( Box( 250, 400, "science.png") )
    while done:
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():    
            if event.type == QUIT:
                done = False
                return False
            if event.type == MOUSEBUTTONDOWN:
                posMouse = pygame.mouse.get_pos()
                for i in range(0,2):
                    if posMouse[0] < boxes[i].x + 200 and posMouse[0] > boxes[i].x and posMouse[1] < boxes[i].y + 100 and posMouse[1] > boxes[i].y:
                        if i == 0:
                            if play("maths.txt") == False:
                                return False
                            pygame.mouse.set_visible(1)
                        elif i == 1:
                            if play("science.txt") == False:
                                return False
                            pygame.mouse.set_visible(1)
        for i in range(0,2):
            boxes[i].draw()
        pygame.display.flip()
        fpsClock.tick(FPS)
    
def main(argv=None):
    if startMenu() == False:
        pygame.quit()
        return 0

    

if __name__ == '__main__':
    exit(main())

