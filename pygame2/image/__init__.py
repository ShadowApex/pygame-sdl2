#!/usr/bin/python

import sdl2
import pygame2

def load(filename):
    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    sprite = pygame2.display.window.factory.from_image(filename)
    sprite.angle = 0
    if pygame2.display.window.type == "software":
        sprite.original = pygame2.display.window.factory.from_image(filename)
    else:
        sprite.sw_sprite = pygame2.display.window.sw_factory.from_image(filename)

    image = pygame2.Surface(sprite=sprite)

    return image
