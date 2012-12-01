import pygame
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
GRAVITY = 7
MOVEMENT_SPEED = 25

fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption("Jump!")
pygame.mouse.set_visible(0)
# pygame.key.set_repeat(1, 10)

WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

BASELINE = 500 # The "floor" which the character can go no lower than.

catImg = pygame.image.load('../cat.png')
catx = 260
caty = BASELINE

thePlatform = pygame.Rect(150, 300, 150, 50)

verticalSpeed = 0
horizontalSpeed = 0

# Remember if the left arrow or right arrow are currently held down.
# Without these variables, if you lift one key while the other key is 
# already held down, the character will stop moving, instead of the
# desired behaviour which is to move in the opposite direction.
leftKeyPressed  = False
rightKeyPressed = False

done = False
while not done:
  DISPLAYSURF.fill(WHITE)

  pygame.draw.rect(DISPLAYSURF, GREEN, thePlatform)
  DISPLAYSURF.blit(catImg, (catx, caty))


  for event in pygame.event.get():
    # If a key is pressed down...
    if event.type == KEYDOWN:
      # If the left arrow is pressed, change the speed of the character
      if event.key == K_LEFT:
        leftKeyPressed = True
        # Only change the speed if the character is not already moving.
        # (In practice, he can only be moving in the opposite direction)
        if horizontalSpeed == 0:
          horizontalSpeed -= MOVEMENT_SPEED
      # Similarly if the right arrow is pressed
      if event.key == K_RIGHT:
        rightKeyPressed = True
        if horizontalSpeed == 0:
          horizontalSpeed += MOVEMENT_SPEED
      # Space to jump
      if event.key == K_SPACE:
        if caty == BASELINE:
          verticalSpeed += 70 
      if (event.key == K_ESCAPE):
        done = True
    if event.type == KEYUP:
      if event.key == K_LEFT:
        leftKeyPressed = False
        horizontalSpeed = 0
        if rightKeyPressed:
          horizontalSpeed += MOVEMENT_SPEED
      if event.key == K_RIGHT:
        rightKeyPressed = False
        horizontalSpeed = 0
        if leftKeyPressed:
          horizontalSpeed -= MOVEMENT_SPEED

        
  if caty < BASELINE:
    verticalSpeed -= GRAVITY
  caty -= verticalSpeed
  if caty > BASELINE:
    caty = BASELINE
    verticalSpeed = 0

  if catx >= 10 and catx <= 660:
    catx += horizontalSpeed
    if catx < 10:
      catx = 10
    elif catx > 660:
      catx = 660


  

  pygame.display.update()
  fpsClock.tick(FPS)
