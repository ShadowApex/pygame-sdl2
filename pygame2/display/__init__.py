#!/usr/bin/python
"""Window handling module."""

import sdl2.ext
import pygame2

from sdl2 import rect, render
from sdl2.ext.compat import isiterable

try:
    import sdl2.sdlgfx
except:
    pass

window = None

class Window(object):
    def __init__(self, title="Pygame2", size=(800, 600), type="hardware", fullscreen=False):
        self.title = title
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.type = type

        # Create our SDL2 window.
        self.sdl2_window = sdl2.ext.Window(title, size)
        self.sdl2_window.show()
        self.world = sdl2.ext.World()
        self.systems = []
        self.sprites = []

        # Set up our renderer.
        if type == "software":
            self.texture_renderer = None
            self.sprite_renderer = SoftwareRenderer(self.sdl2_window)
            self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        elif type == "hardware":
            self.texture_renderer = sdl2.ext.Renderer(self.sdl2_window)
            self.sprite_renderer = TextureRenderer(self.texture_renderer)
            self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE,
                                                  renderer=self.texture_renderer)
            self.sw_factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

        # Add our renderer as a system that will be called when
        # world.process() is called.
        self.world.add_system(self.sprite_renderer)


    def update(self):

        dt = 0
        for system in self.systems:
            system.process(self, dt)

        #if self.type == "hardware":
        #    self.texture_renderer.clear()

        if self.sprites:
            self.sprite_renderer.render(self.sprites)
        #self.world.process()
        self.sdl2_window.refresh()


    def blit(self, surface, position):
        sprite = surface.sprite
        if not position:
            position = [sprite.x, sprite.y]
        else:
            sprite.x = position[0]
            sprite.y = position[1]

        self.sprite_renderer.render(sprite)


    def toggle_fullscreen(self):
        sdl2.SDL_SetWindowFullscreen(self.sdl2_window,
                                     sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)


    def set_caption(self, title):
        self.title = title
        self.sdl2_window.title = title


    def set_icon(self, icon_path):
        pass


    def add_system(self, system):
        self.systems.append(system)


    def fill(self, color):
        if self.type == "software":
            # Fill the screen with black every frame.
            sdl2.ext.fill(self.sprite_renderer.surface,
                          sdl2.ext.Color(color[0], color[1], color[2]))

        elif self.type == "hardware":
            self.texture_renderer.clear(color)


    def get_rect(self):
        rect = pygame2.Rect(0, 0, self.width, self.height)

        return rect


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        # Fill the screen with black every frame.
        #sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))

        # If we're using software rendering, do rotation using sdlgfx.
        if isiterable(components):
            sprites = []
            for sprite in components:
                rotozoom = sdl2.sdlgfx.rotozoomSurface
                surface = rotozoom(sprite.original.surface,
                                   sprite.angle,
                                   1.0,
                                   1).contents
                sdl2.SDL_FreeSurface(sprite.surface)
                sprite.surface = surface
                sprites.append(sprite)
            components = sprites
        else:
            surface = sdl2.sdlgfx.rotozoomSurface(components.original.surface,
                                                  components.angle,
                                                  1.0,
                                                  1).contents
            sdl2.SDL_FreeSurface(components.surface)
            components.surface = surface
    
        super(SoftwareRenderer, self).render(components)


class TextureRenderer(sdl2.ext.TextureSpriteRenderSystem):
    def __init__(self, target):
        super(TextureRenderer, self).__init__(target)

    def render(self, sprites, x=None, y=None):
        """Overrides the render method of sdl2.ext.TextureSpriteRenderSystem to
        use "SDL_RenderCopyEx" instead of "SDL_RenderCopy" to allow sprite
        rotation:

        http://wiki.libsdl.org/SDL_RenderCopyEx
        """
        r = rect.SDL_Rect(0, 0, 0, 0)
        if isiterable(sprites):
            rcopy = render.SDL_RenderCopyEx
            renderer = self.sdlrenderer
            x = x or 0
            y = y or 0
            for sp in sprites:
                r.x = x + sp.x
                r.y = y + sp.y
                r.w, r.h = sp.size
                if rcopy(renderer, sp.texture, None, r, sp.angle, None, render.SDL_FLIP_NONE) == -1:
                    raise SDLError()
        else:
            r.x = sprites.x
            r.y = sprites.y
            r.w, r.h = sprites.size
            if x is not None and y is not None:
                r.x = x
                r.y = y
            render.SDL_RenderCopyEx(self.sdlrenderer,
                                    sprites.texture,
                                    None,
                                    r,
                                    sprites.angle,
                                    None,
                                    render.SDL_FLIP_NONE)
        render.SDL_RenderPresent(self.sdlrenderer)


def create(size=(800, 600), title="Pygame2", type="hardware"):
    return set_mode(size, title, type)


def set_mode(size=(800, 600), title="Pygame2", type="hardware"):
    global window
    if not window:
        window = Window(title, size, type)
    else:
        raise Exception("Error: Cannot create a window after one has already been created.")

    return window


def set_caption(title):
    global window
    if window:
        window.set_caption(title)
    else:
        window = Window(title)

    return window


def update():
    global window
    window.update()


def flip():
    update()


def get_surface():
    global window
    return window


def set_mode(size, fullscreen=0, depth=32):
    global window
    if window:
        sdl2.SDL_SetWindowSize(window.sdl2_window.window, size[0], size[1])
        window.size = size
        window.width = size[0]
        window.height = size[1]
    else:
        window = Window(size=size)

    return window
