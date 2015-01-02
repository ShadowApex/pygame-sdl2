#!/usr/bin/python

import sdl2

pressed = []
for i in range(100):
    pressed.append(0)

def get_pressed():
    #print "Getting pressed keys:"
    results = sdl2.keyboard.SDL_GetKeyboardState(None)
    #print results.contents.value
    #print dir(results.contents)
    #print "Dun"

    return pressed
