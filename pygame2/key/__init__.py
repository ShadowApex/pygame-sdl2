#!/usr/bin/python

import sdl2
import ctypes

pressed = []
for i in range(100):
    pressed.append(0)

def get_pressed():
    num_keys = ctypes.c_int()
    pressed = sdl2.keyboard.SDL_GetKeyboardState(num_keys)
    keys = []
    for index in range(num_keys.value):
        keys.append(pressed[index])

    return keys
