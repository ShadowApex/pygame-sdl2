Pygame-SDL2
===========

Pygame-SDL2 is a project that aims to be a drop-in replacement for Pygame
that uses pysdl2 as its backend, and aims to create an even simpler API
than Pygame for creating games. To start using Pygame-SDL2 with your existing
Pygame project, all you need to do is change your pygame import from this:

```import pygame```

to this:

```import pygame2 as pygame```

Right now only basic pygame methods have been re-implemented, and thus
is not yet appropriate to fully replace Pygame at this time.


Requirements
============

* pysdl2
* pymunk
