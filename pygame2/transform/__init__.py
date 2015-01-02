#!/usr/bin/python

import sdl2
import sdl2.sdlgfx

from sdl2 import surface

import pygame2


def scale(surface, size, dest_sprite=None, resample=0):
    """Scale an image using python's imaging library."""

    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    sprite = surface.sprite

    # Resize the image using PIL
    try:
        img = sprite.pil.resize(size, resample)
    except AttributeError:
        print "ERROR: This surface does not have a PIL object! Resizing image failed."
        return surface

    # Create an SDL2 surface from our sprite.
    surface, pil_surface = pygame2.image.load_image(img)

    # Create a new sprite from the surface.
    scaled_sprite = pygame2.display.window.factory.from_surface(surface)
    scaled_sprite.angle = sprite.angle
    scaled_sprite.pil = pil_surface

    # If we're using a software renderer, keep an original for rotation.
    if pygame2.display.window.type == "software":
        scaled_sprite.original = pygame2.display.window.factory.from_surface(surface, True)
    else:
        scaled_sprite.sw_sprite = pygame2.display.window.sw_factory.from_surface(surface, True)

    image = pygame2.Surface(sprite=scaled_sprite)

    return image


def copy(surface):
    
    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    sprite = surface.sprite
    
    # Resize the image using PIL
    img = sprite.pil

    # Create an SDL2 surface from our sprite.
    surface, pil_surface = pygame2.image.load_image(img)

    # Create a new sprite from the surface.
    new_sprite = pygame2.display.window.factory.from_surface(surface)
    new_sprite.angle = sprite.angle
    new_sprite.pil = pil_surface

    # If we're using a software renderer, keep an original for rotation.
    if pygame2.display.window.type == "software":
        new_sprite.original = pygame2.display.window.factory.from_surface(surface, True)
    else:
        new_sprite.sw_sprite = pygame2.display.window.sw_factory.from_surface(surface, True)

    image = pygame2.Surface(sprite=new_sprite)

    return image

