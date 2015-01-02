#!/usr/bin/python
import pygame2 as pygame
import sys
import time
from pygame2.locals import *

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

asteroid = pygame.image.load('asteroid_1.png')
asteroid = pygame.transform.scale(asteroid, (100, 100))

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    screen.blit(asteroid, (50, 50))
    pygame.display.update()

