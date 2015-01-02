#!/usr/bin/python
"""Main pygame2 module."""

import sys

import sdl2
import sdl2.ext
from sdl2.ext.compat import isiterable

import pygame2.display
import pygame2.key
import pygame2.image
import pygame2.app
import pygame2.event
import pygame2.joystick
import pygame2.transform
import pygame2.time
import pygame2.font


# Temporary Pygame constants. Will replace these with
# the real constants in the future.
QUIT = 0
KEYDOWN = 1
KEYUP = 2
K_LCTRL = 3
K_RCTRL = 3
K_LALT = 4
K_RALT = 5
K_LSHIFT = 6
K_RSHIFT = 7

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

        self.size = size
        self.alpha = 255

    def convert(self):
        # This does nothing and is here for pygame compatibility.
        return self

    def convert_alpha(self):
        # This does nothing and is here for pygame compatibility.
        return self

    def fill(self, color):
        # If a sprite hasn't been created, create an empty one.
        if not self.sprite:

            # Create a sprite.
            sprite = pygame2.display.window.factory.from_color(color, self.size)
            sprite.angle = 0

            # If we're using a software renderer, keep an original for rotation.
            if pygame2.display.window.type == "software":
                sprite.original = pygame2.display.window.factory.from_color(color, self.size)
            else:
                sprite.sw_sprite = pygame2.display.window.sw_factory.from_color(color, self.size)

            self.sprite = sprite

        else:
            sdl2.ext.fill(self.sprite, color)


    def get_alpha(self):
        # first, which band is the alpha channel?
        try:
            alpha_index = self.sprite.pil.getbands().index('A')
        except ValueError:
            return None # no alpha channel, presumably

        return self.alpha

    def get_size(self):
        return self.sprite.size

    def get_width(self):
        return self.sprite.size[0]

    def get_height(self):
        return self.sprite.size[1]

    def copy(self):
        print "  copying surface!"
        return pygame2.transform.copy(self)

    def set_alpha(self, value):
        # If this is a sw renderer, simply set the alpha of the surface.
        if pygame2.display.window.type == "software":
            sdl2.surface.SDL_SetSurfaceAlphaMod(self.sprite.surface, int(value))
        else:
            # We need to re-create our hardware surface from the surface
            sdl2.SDL_SetTextureAlphaMod(self.sprite.texture, int(value))

    def set_colorkey(self, colorkey):
        # Right now this does nothing
        pass


    def subsurface(self, rect):

        if len(rect) == 3:
            rect = (rect[0][0], rect[0][1], rect[1], rect[2])
        elif len(rect) == 2:
            rect = (rect[0][0], rect[0][1], rect[1][0], rect[1][1])

        if pygame2.display.window.type == "software":
            surface = sdl2.ext.subsurface(self.sprite.surface, rect)
            sprite = pygame2.display.window.factory.from_surface(surface)
            sprite.original = pygame2.display.window.factory.from_surface(surface)
        else:
            # https://wiki.libsdl.org/SDL_RenderCopyEx
            # RenderCopyEx allows you to specify the Rect of the source texture
            # to render. We may want to use this instead.
            surface = sdl2.ext.subsurface(self.sprite.sw_sprite.surface, rect)
            sprite = pygame2.display.window.factory.from_surface(surface)
            sprite.sw_sprite = pygame2.display.window.sw_factory.from_surface(surface)

        sprite.angle = self.sprite.angle
        sprite.pil = self.sprite.pil.crop(rect) # Dirty hack to get a PIL object of subsurf.

        return Surface(sprite=sprite)
            


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
        else:
            rect = sdl2.SDL_Rect(self.left, self.top, self.width, self.height)

        if sdl2.SDL_HasIntersection(self.rect, rect):
            return True
        else:
            return False
