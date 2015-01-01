#!/usr/bin/python
"""Main pygame2 module."""

import sdl2
import sdl2.ext
from sdl2.ext.compat import isiterable

import pygame2.display
import pygame2.image
import pygame2.app
import pygame2.event
import pygame2.joystick
import pygame2.transform

def init():
    sdl2.ext.init()


def quit():
    sdl2.ext.quit()


class Surface(object):
    def __init__(self, size=(0, 0), flags=0, depth=0, masks=None, sprite=None):
        if sprite:
            self.sprite = sprite
        else:
            self.sprite = None

    def get_size(self):
        return self.sprite.size

    def get_width(self):
        return self.sprite.size[0]

    def get_height(self):
        return self.sprite.size[1]

    def copy(self):
        print "  copying surface!"
        return pygame2.transform.copy(self)


class Rect(object):
    def __init__(self, left=0, top=0, width=0, height=0):
        if isiterable(left):
            self.left = left[0]
            self.top = left[1]
            self.width = top[0]
            self.height = top[1]
        else:
            self.left = left
            self.top = top
            self.width = width
            self.height = height

        self.rect = sdl2.SDL_Rect(left, top, width, height)


    def colliderect(self, rect):
        if isiterable(rect):
            rect = sdl2.SDL_Rect(rect[0], rect[1], rect[2], rect[3])

        if sdl2.SDL_HasIntersection(self.rect, rect):
            return True
        else:
            return False
