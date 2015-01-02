#!/usr/bin/python

import time

class Clock(object):
    def __init__(self):
        self.time_old = time.time()
        self.time_elapsed = 1

    def tick(self, framerate=0):
        time_new = time.time()
        time_elapsed = time_new - self.time_old
        self.time_old = time_new
        self.time_elapsed = time_elapsed

        if framerate:
            time.sleep(1./framerate)

        # Give our time elapsed in milliseconds.
        return time_elapsed * 1000

    def tick_busy_loop(self):
        pass

    def get_fps(self):
        return 1./self.time_elapsed
