#!/usr/bin/python

import sdl2
import sdl2.sdlgfx

from sdl2 import surface

import pygame2
#import pygame2.display


def scale(surface, size, dest_sprite=None):
    """Right now this only scales proportionally by width."""

    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    sprite = surface.sprite

    # Get the surface depending on our rendering type.
    if pygame2.display.window.type == "software":
        scaled_sprite = pygame2.display.window.factory.from_surface(sprite.surface)
        original_surface = sprite.surface

    # If this is a hardware surface, we need to convert it to a software
    # surface, perform the scaling, and then convert it back to a texture.
    else:
        scaled_sprite = pygame2.display.window.sw_factory.from_surface(sprite.sw_sprite.surface)
        original_surface = sprite.sw_sprite.surface

    # Find out how much we need to scale the sprite by.
    scale = float(size[0]) / float(sprite.size[0])

    # Create a new sprite that we'll scale.
    scaled_sprite.x = sprite.x
    scaled_sprite.y = sprite.y
    scaled_sprite.angle = sprite.angle

    rotozoom = sdl2.sdlgfx.rotozoomSurface
    surface = rotozoom(original_surface,
                       0,
                       scale,
                       1).contents

    sdl2.SDL_FreeSurface(scaled_sprite.surface)
    scaled_sprite.surface = surface

    if pygame2.display.window.type == "software":
        if dest_sprite:
            dest_sprite = scaled_sprite

        return scaled_sprite

    else:
        scaled_hw_sprite = pygame2.display.window.factory.from_surface(scaled_sprite.surface)
        scaled_hw_sprite.sw_sprite = pygame2.display.window.factory.from_surface(scaled_sprite.surface)
        scaled_hw_sprite.x = scaled_sprite.x
        scaled_hw_sprite.y = scaled_sprite.y
        scaled_hw_sprite.angle = scaled_sprite.angle

        if dest_sprite:
            dest_sprite = scaled_hw_sprite

        return scaled_hw_sprite


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
