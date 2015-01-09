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
        """An object used to create SDL2 windows.

        The *Window* object contains backwards compatible methods for the
        pygame display and creates a simple way to render surfaces to the
        screen.

        Args:
          title (str): The title of the window.
          size (tuple of int, optional): The size of the window in pixels,
            defaults to (800, 600).
          type (str, optional): The type of SDL2 window to create. Can be
            either "hardware" or "software", defaults to "hardware".
          fullscreen (boolean, optional): Whether or not the window is
            fullscreen, defaults to False.

        """
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
        self.to_blit = []

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
        """Updates the contents of the window.

        When this method is called, we render all sprites that have been added
        to our "to_blit" list.

        Args:
          None

        Returns:
          None

        """
        dt = 0
        for system in self.systems:
            system.process(self, dt)

        #if self.type == "hardware":
        #    self.texture_renderer.clear()

        #if self.sprites:
        #    self.sprite_renderer.render(self.sprites)
        if self.to_blit:
            self.sprite_renderer.render(self.to_blit)
            self.to_blit = []

        #self.world.process()
        self.sdl2_window.refresh()


    def blit(self, surface, position):
        """Adds a sprite to our list of sprites to be drawn on update.

        This method allows backwards compatibility of pygame projects by
        setting the sprite's position and adding it to our "to_blit" list.

        Args:
          surface (pygame2.Surface): The surface object containing the sprite
            to draw on the screen.
          position (tuple of int): The (x, y) position on the screen to draw
            the sprite at.

        Returns:
          None

        """
        sprite = surface.sprite
        if not position:
            position = [sprite.x, sprite.y]
        else:
            sprite.x = position[0]
            sprite.y = position[1]

        #self.sprite_renderer.render(sprite)
        self.to_blit.append(sprite)


    def toggle_fullscreen(self):
        """Toggles fullscreen.

        This method toggles fullscreen using the SDL2_SetWindowFullscreen
        function.

        Args:
          None

        Returns:
          None

        """
        sdl2.SDL_SetWindowFullscreen(self.sdl2_window,
                                     sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)


    def set_caption(self, title):
        """Sets the title of the SDL2 window.

        This method allows backwards compatibility with pygame.

        Args:
          title (str): The title of the window.

        Returns:
          None

        """
        self.title = title
        self.sdl2_window.title = title


    def set_icon(self, icon_path):
        """Sets the icon of the window.

        This method allows backwards compatibility with pygame.

        Args:
          icon_path (str): Path to the icon file to use.

        Returns:
          None

        """
        pass


    def add_system(self, system):
        """Adds an object with a "process" method that is executed on update.

        This method employs a new way to define "systems" that will be called
        whenever the window's "update" method is called.

        Args:
          system (object): An object with a "process" method.

        """
        self.systems.append(system)


    def fill(self, color):
        """Fills the window with an RGB(A) color.

        This method provides a backwards compatible method for filling the
        screen with a particular color.

        Args:
          color (tuple of int): The (r, g, b, a) color values to fill the
            screen.

        Returns:
          None

        """
        if self.type == "software":
            # Fill the screen with black every frame.
            sdl2.ext.fill(self.sprite_renderer.surface,
                          sdl2.ext.Color(color[0], color[1], color[2]))

        elif self.type == "hardware":
            self.texture_renderer.clear(color)


    def get_rect(self):
        """Gets the rectangle of the current window.

        This method provides a pygame-compatible way to get the rectangle
        of the current window.

        Args:
          None

        Returns:
          A pygame2.Rect object.

        """
        rect = pygame2.Rect(0, 0, self.width, self.height)

        return rect


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):

    def __init__(self, window):
        """Creates an SDL2 software renderer used for software rendering.

        SDL2 is capable of using either software or texture-based rendering.
        Texture rendering uses hardware acceleration to draw 2d sprites,
        while software rendering uses the CPU to draw 2d sprites.

        Args:
          window (pygame2.display.Window): The pygame2 window object.

        """
        super(SoftwareRenderer, self).__init__(window)


    def render(self, components):
        """Renders a sprite or list of sprites to the screen.

        This is a modified version of the original pysdl2 software render
        method, but includes the ability to rotate sprites using sdlgfx.
        Note that sdlgfx must be installed for this method to work.

        Args:
          components (SDL2 Sprite or List): A sprite or list of sprites to
            render to the screen.

        Returns:
          None

        """
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
        """Creates an SDL2 texture renderer used for hardware rendering.

        SDL2 is capable of using either software or texture-based rendering.
        Texture rendering uses hardware acceleration to draw 2d sprites,
        while software rendering uses the CPU to draw 2d sprites.

        Args:
          target (sdl2.ext.Renderer): An SDL2 texture renderer object.

        """
        super(TextureRenderer, self).__init__(target)


    def render(self, sprites, x=None, y=None):
        """Renders a sprite or list of sprites to the screen.

        This method overrides the render method of the
        sdl2.ext.TextureSpriteRenderSystem to use "SDL_RenderCopyEx" instead 
        of "SDL_RenderCopy" to allow sprite rotation:
        http://wiki.libsdl.org/SDL_RenderCopyEx

        Args:
          sprites (SDL2 Sprite or List): A sprite or list of sprites to
            render to the screen.
          x (int, optional): X position to render the sprite, defaults to None
          y (int, optional): Y position to render the sprite, defaults to None

        Returns:
          None

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
    """Creates an SDL2 window.

    This method provides a pygame-like way to create a window.

    Args:
      size (tuple of int, optional): An (x, y) size of the window to create,
        defaults to (800, 600)
      title (str, optional): The title of the window, defaults to "Pygame2"
      type (str, optional): The type of sprite renderer to use. Can be either
        "software" or "hardware". Defaults to "hardware".

    Returns:
      A pygame2.display.Window object.

    """
    return set_mode(size, title, type)


def set_mode(size=(800, 600), title="Pygame2", type="hardware"):
    """Creates an SDL2 window with the provided size.

    This method provides a pygame-compatible way to create a window.

    Args:
      size (tuple of int, optional): An (x, y) size of the window to create,
        defaults to (800, 600)
      title (str, optional): The title of the window, defaults to "Pygame2"
      type (str, optional): The type of sprite renderer to use. Can be either
        "software" or "hardware". Defaults to "hardware".

    Returns:
      A pygame2.display.Window object.

    """
    global window
    if not window:
        window = Window(title, size, type)
    else:
        raise Exception("Error: Cannot create a window after one has already been created.")

    return window


def set_caption(title):
    """Sets the title of the current window.

    This method provides a pygame-compatible way to set the window caption.

    Args:
      title (str): The title of the window.

    Returns:
      A pygame2.display.Window object.

    """
    global window
    if window:
        window.set_caption(title)
    else:
        window = Window(title)

    return window


def update():
    """Updates the contents of the current window.

    This method provides a pygame-compatible way to refresh the window.

    Args:
      None

    Returns:
      None

    """
    global window
    window.update()


def flip():
    """Updates the contents of the current window.

    This method provides a pygame-compatible way to refresh the window.

    Args:
      None

    Returns:
      None

    """
    update()


def get_surface():
    """Returns a copy of the current window object.

    This method provides a pygame-compatible method to get the current window.

    Args:
      None

    Returns:
      A pygame2.display.Window object.

    """
    global window
    return window


def set_mode(size, fullscreen=0, depth=32):
    """Sets the resolution of the window.

    This method provides a pygame-compatible way to create or set the window
    size.

    Args:
      size (tuple of int): The (x, y) size of the window.
      fullscreen (boolean, optional): Whether or not to set the window to
        fullscreen mode, defaults to 0.
      depth (int, optional): Legacy argument for pygame compatibility, defaults
        to 32.

    Returns:
      A pygame2.display.Window object.

    """
    global window
    if window:
        sdl2.SDL_SetWindowSize(window.sdl2_window.window, size[0], size[1])
        window.size = size
        window.width = size[0]
        window.height = size[1]
    else:
        window = Window(size=size)

    return window
