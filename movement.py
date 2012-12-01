from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pygame
from pygame.locals import *

# Constants:
FPS = 60                # frames per second setting
GRAVITY = 7             # The speed at which the character falls
MOVEMENT_SPEED = 25     # The speed at which the char moves left or right.
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BASELINE = 500     # The "floor" which the character can go no lower than.
CHAR_SPRITE = 'cat.png' # The sprite for the player character

fpsClock = pygame.time.Clock()
thePlatform = pygame.Rect(150, 300, 150, 50)
class Character:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.verticalSpeed = 0
        self.horizontalSpeed = 0
        self.img = pygame.image.load(img)


def main(argv=None):
  pygame.init()

  # Create the display window:
  DISPLAYSURF = pygame.display.set_mode((800,600))
  pygame.display.set_caption("Jump!")
  pygame.mouse.set_visible(0)

  # Load the player character:
  theChar = Character(260, BASELINE, CHAR_SPRITE)

  # Remember if the left arrow or right arrow are currently held down.
  # Without these variables, if you lift one key while the other key is 
  # already held down, the character will stop moving, instead of the
  # desired behaviour which is to move in the opposite direction.
  leftKeyPressed  = False
  rightKeyPressed = False

  done = False
  while not done:
    print(1)
    DISPLAYSURF.fill(WHITE)

    pygame.draw.rect(DISPLAYSURF, GREEN, thePlatform)
    DISPLAYSURF.blit(theChar.img, (theChar.x, theChar.y))


    for event in pygame.event.get():
      # If a key is pressed down...
      if event.type == KEYDOWN:
        # If the left arrow is pressed, change the speed of the character
        if event.key == K_LEFT:
          leftKeyPressed = True
          # Only change the speed if the character is not already moving.
          # (In practice, he can only be moving in the opposite direction)
          if theChar.horizontalSpeed == 0:
            theChar.horizontalSpeed -= MOVEMENT_SPEED
        # Similarly if the right arrow is pressed
        if event.key == K_RIGHT:
          rightKeyPressed = True
          if theChar.horizontalSpeed == 0:
            theChar.horizontalSpeed += MOVEMENT_SPEED
        # Space to jump
        if event.key == K_SPACE:
          if theChar.y == BASELINE:
            theChar.verticalSpeed += 70 
        if (event.key == K_ESCAPE):
          done = True
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

          
    if theChar.y < BASELINE:
      theChar.verticalSpeed -= GRAVITY
    theChar.y -= theChar.verticalSpeed
    if theChar.y > BASELINE:
      theChar.y = BASELINE
      theChar.verticalSpeed = 0

    if theChar.x >= 10 and theChar.x <= 660:
      theChar.x += theChar.horizontalSpeed
      if theChar.x < 10:
        theChar.x = 10
      elif theChar.x > 660:
        theChar.x = 660

    pygame.display.update()
    fpsClock.tick(FPS)


  pygame.quit()
  return 0


if __name__ == '__main__':
  exit(main())

