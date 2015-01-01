#!/usr/bin/python

import sdl2
import sdl2.ext


def get():
    events = []
    sdl2_events = sdl2.ext.get_events()
    for event in sdl2_events:
        events.append(event)

    return events
