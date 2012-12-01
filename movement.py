import pygame
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
GRAVITY = 10
MOVEMENT_SPEED = 30

fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption("Jump!")
pygame.mouse.set_visible(0)
# pygame.key.set_repeat(1, 10)


BASELINE = 500
WHITE = (255, 255, 255)
catImg = pygame.image.load('../cat.png')
catx = 10
caty = BASELINE

verticalSpeed = 0
horizontalSpeed = 0

done = False
while not done:
  DISPLAYSURF.fill(WHITE)

  DISPLAYSURF.blit(catImg, (catx, caty))

  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_LEFT:
        horizontalSpeed -= MOVEMENT_SPEED
      if event.key == K_RIGHT:
        horizontalSpeed += MOVEMENT_SPEED
      # Space to jump
      if event.key == K_SPACE:
        if caty == BASELINE:
          verticalSpeed += 80 
      if (event.key == K_ESCAPE):
        done = True
    if event.type == KEYUP:
      if event.key == K_LEFT or event.key == K_RIGHT:
        horizontalSpeed = 0

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
