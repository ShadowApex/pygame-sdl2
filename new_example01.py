#!/usr/bin/python

import pygame2

pygame2.init()
window = pygame2.display.create()

asteroid = pygame2.image.load('asteroid_1.png')
asteroid.x = 50
asteroid.y = 100
asteroid.angle = 45
asteroid.depth = 10
window.sprites.append(asteroid)


class EventSystem(object):
    def process(self, display, dt):
        #events = pygame2.event.get_events()
        pass

class StateSystem(object):
    def process(self, display, dt):
        display.sprites[0].angle += 1

window.add_system(EventSystem())
window.add_system(StateSystem())

pygame2.app.run()
