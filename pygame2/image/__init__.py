#!/usr/bin/python

import sdl2
import pygame2

from sdl2.ext.common import SDLError
from sdl2.ext.compat import UnsupportedError, byteify
from sdl2 import endian, surface, pixels

_HASPIL = True
from PIL import Image


def load(filename):
    if not pygame2.display.window:
        raise Exception("Error: Window has not yet been created.")

    # Load the image using PIL so we get the SDL surface and PIL object.
    surface, pil_surface = load_image(filename)

    # Create a sprite.
    sprite = pygame2.display.window.factory.from_surface(surface, True)
    sprite.angle = 0
    sprite.pil = pil_surface

    # If we're using a software renderer, keep an original for rotation.
    if pygame2.display.window.type == "software":
        sprite.original = pygame2.display.window.factory.from_image(filename)
    else:
        sprite.sw_sprite = pygame2.display.window.sw_factory.from_image(filename)

    image = pygame2.Surface(sprite=sprite)

    return image




def load_image(fname, enforce=None):
    """Creates a SDL_Surface from an image file.

    ** This is an altered version of the load_image method from pysdl2.

    This function makes use of the Python Imaging Library, if it is available
    on the target execution environment. The function will try to load the
    file via sdl2 first. If the file could not be loaded, it will try
    to load it via sdl2.sdlimage and PIL.

    You can force the function to use only one of them, by passing the enforce
    as either "PIL" or "SDL".

    Note: This will call sdl2.sdlimage.init() implicitly with the default
    arguments, if the module is available and if sdl2.SDL_LoadBMP() failed to
    load the image.

    fname can be either a string of the file to load or a PIL image object.

    """

    if enforce is not None and enforce not in ("PIL", "SDL"):
        raise ValueError("enforce must be either 'PIL' or 'SDL', if set")

    if type(fname) is str:
        name = byteify(fname, "utf-8")

    if enforce == "PIL" and not _HASPIL:
        raise UnsupportedError(load_image, "cannot use PIL (not found)")

    imgsurface = None

    if enforce != "SDL" and _HASPIL and not imgsurface:
        if type(fname) is str:
            image = Image.open(fname)
        else:
            image = fname
        mode = image.mode
        width, height = image.size
        rmask = gmask = bmask = amask = 0
        if mode in ("1", "L", "P"):
            # 1 = B/W, 1 bit per byte
            # "L" = greyscale, 8-bit
            # "P" = palette-based, 8-bit
            pitch = width
            depth = 8
        elif mode == "RGB":
            # 3x8-bit, 24bpp
            if endian.SDL_BYTEORDER == endian.SDL_LIL_ENDIAN:
                rmask = 0x0000FF
                gmask = 0x00FF00
                bmask = 0xFF0000
            else:
                rmask = 0xFF0000
                gmask = 0x00FF00
                bmask = 0x0000FF
            depth = 24
            pitch = width * 3
        elif mode in ("RGBA", "RGBX"):
            # RGBX: 4x8-bit, no alpha
            # RGBA: 4x8-bit, alpha
            if endian.SDL_BYTEORDER == endian.SDL_LIL_ENDIAN:
                rmask = 0x000000FF
                gmask = 0x0000FF00
                bmask = 0x00FF0000
                if mode == "RGBA":
                    amask = 0xFF000000
            else:
                rmask = 0xFF000000
                gmask = 0x00FF0000
                bmask = 0x0000FF00
                if mode == "RGBA":
                    amask = 0x000000FF
            depth = 32
            pitch = width * 4
        else:
            # We do not support CMYK or YCbCr for now
            raise TypeError("unsupported image format")

        pxbuf = image.tostring()
        imgsurface = surface.SDL_CreateRGBSurfaceFrom(pxbuf, width, height,
                                                      depth, pitch, rmask,
                                                      gmask, bmask, amask)
        if not imgsurface:
            raise SDLError()
        imgsurface = imgsurface.contents
        # the pixel buffer must not be freed for the lifetime of the surface
        imgsurface._pxbuf = pxbuf

        if mode == "P":
            # Create a SDL_Palette for the SDL_Surface
            def _chunk(seq, size):
                for x in range(0, len(seq), size):
                    yield seq[x:x + size]

            rgbcolors = image.getpalette()
            sdlpalette = pixels.SDL_AllocPalette(len(rgbcolors) // 3)
            if not sdlpalette:
                raise SDLError()
            sdlpalette = sdlpalette.contents
            SDL_Color = pixels.SDL_Color
            for idx, (r, g, b) in enumerate(_chunk(rgbcolors, 3)):
                sdlpalette.colors[idx] = SDL_Color(r, g, b)
            ret = surface.SDL_SetSurfacePalette(imgsurface, sdlpalette)
            # This will decrease the refcount on the palette, so it gets
            # freed properly on releasing the SDL_Surface.
            pixels.SDL_FreePalette(sdlpalette)
            if ret != 0:
                raise SDLError()

    return imgsurface, image
