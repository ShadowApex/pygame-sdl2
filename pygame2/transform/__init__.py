#!/usr/bin/python

import sdl2
import sdl2.sdlgfx

from sdl2 import surface

import pygame2


def scale(surface, size, dest_sprite=None, resample=0):
    """Right now this only scales proportionally by width."""

    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    sprite = surface.sprite

    # Resize the image using PIL
    img = sprite.pil.resize(size, resample)

    # Create an SDL2 surface from our sprite.
    surface, pil_surface = pygame2.image.load_image(img)

    # Create a new sprite from the surface.
    scaled_sprite = pygame2.display.window.factory.from_surface(surface, True)
    scaled_sprite.angle = 0
    scaled_sprite.pil = pil_surface

    # If we're using a software renderer, keep an original for rotation.
    #if pygame2.display.window.type == "software":
    #    sprite.original = pygame2.display.window.factory.from_image(filename)
    #else:
    #    sprite.sw_sprite = pygame2.display.window.sw_factory.from_image(filename)

    image = pygame2.Surface(sprite=scaled_sprite)


    return image


def copy(surface):
    
    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    sprite = surface.sprite
    
    # Get the surface depending on our rendering type.
    if pygame2.display.window.type == "software":
        sprite_copy = pygame2.display.window.factory.from_surface(sprite.surface)

    # If this is a hardware surface, we need to convert it to a software
    # surface, perform the scaling, and then convert it back to a texture.
    else:
        sprite_copy = pygame2.display.window.factory.from_surface(sprite.sw_sprite.surface)
        sprite_copy.sw_sprite = pygame2.display.window.sw_factory.from_surface(sprite.sw_sprite.surface)

    sprite_copy.x = sprite.x
    sprite_copy.y = sprite.y
    sprite_copy.angle = sprite.angle

    return pygame2.Surface(sprite=sprite_copy)
