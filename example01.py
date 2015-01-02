#!/usr/bin/python
import pygame2 as pygame
import sys
import time
from pygame2.locals import *

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

# Loading images and scaling.
asteroid = pygame.image.load('asteroid_1.png')
asteroid = pygame.transform.scale(asteroid, (100, 100))

# Copying surfaces.
asteroid2 = asteroid.copy()

# Creating and scaling subsurfaces.
asteroid_subsurface = asteroid.subsurface((10, 10, 50, 50))
asteroid_subsurface = pygame.transform.scale(asteroid_subsurface, (10, 10))


while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    screen.blit(asteroid, (0, 0))
    screen.blit(asteroid2, (300, 200))
    screen.blit(asteroid_subsurface, (200, 150))
    pygame.display.update()




