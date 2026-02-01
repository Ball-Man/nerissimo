import math

import desper
import sdl2

import numpy as np

from . import graphics
from .log import logger

ON_WIN_EVENT = 'on_win'


class Velocity():
    """Velociy component."""

    def __init__(self, x, y):
        self.value = desper.math.Vec2(x, y)


@desper.event_handler('on_key_down', 'on_key_up')
class UserControlled(desper.Controller):
    """Adjust velocity based on user input."""
    velocity = desper.ComponentReference(Velocity)

    def on_key_down(self, sym):
        logger.info('Received %d', sym)

        new_x, new_y = self.velocity.value

        if sym == sdl2.SDL_SCANCODE_LEFT or sym == sdl2.SDL_SCANCODE_RIGHT:
            new_y = 0

        if sym == sdl2.SDL_SCANCODE_UP or sym == sdl2.SDL_SCANCODE_DOWN:
            new_x = 0

        self.velocity.value = desper.math.Vec2(new_x, new_y)

        if sym == sdl2.SDL_SCANCODE_LEFT:
            self.velocity.value += (0, -10)
        if sym == sdl2.SDL_SCANCODE_RIGHT:
            self.velocity.value += (0, 10)
        if sym == sdl2.SDL_SCANCODE_UP:
            self.velocity.value += (-10, 0)
        if sym == sdl2.SDL_SCANCODE_DOWN:
            self.velocity.value += (10, 0)

    def on_key_up(self, sym):
        if sym == sdl2.SDL_SCANCODE_LEFT or sym == sdl2.SDL_SCANCODE_RIGHT:
            self.velocity.value = desper.math.Vec2(self.velocity.value[0], 0)
        if sym == sdl2.SDL_SCANCODE_UP or sym == sdl2.SDL_SCANCODE_DOWN:
            self.velocity.value = desper.math.Vec2(0, self.velocity.value[1])


class VelocityProcessor(desper.Processor):
    """Add velocity to transform."""

    def process(self, dt):
        for entity, velocity in self.world.get(Velocity):
            transform = self.world.get_component(entity, desper.Transform2D)

            if __debug__:
                old_position = transform.position

            transform.position += velocity.value * (dt, dt)

            if __debug__:
                new_round_pos_diff = round(old_position) - round(transform.position)
                if abs(new_round_pos_diff[0]) > 1 or abs(new_round_pos_diff[1]) > 1:
                    logger.warning('Velocity of entity %d surpassing 1 pixel per frame (%s)',
                                   entity, velocity.value * (dt, dt))


class WinConditionProcessor(desper.Processor):
    """Dispatch :attr:`ON_WIN_EVENT` when whole screen is black."""
    _enabled = True

    def __init__(self, screen_surface_array: np.ndarray):
        self.screen_surface_array = screen_surface_array

    def process(self, dt):
        if not self._enabled:
            return

        if np.count_nonzero(self.screen_surface_array) == 0:
            logger.info('Win')
            self._enabled = False
            self.world.dispatch(ON_WIN_EVENT)


@desper.event_handler(desper.ON_UPDATE_EVENT_NAME)
class Oscillate(desper.Controller):
    transform = desper.ComponentReference(desper.Transform2D)
    _time = 0

    def __init__(self, amplitude, freq):
        self.amplitude = amplitude
        self.freq = freq

    def on_add(self, *args):
        super().on_add(*args)
        self.base = self.transform.position[0]

    def on_update(self, dt):
        self._time += dt

        self.transform.position = desper.math.Vec2(self.base + self.amplitude * math.cos(self._time * self.freq),
                                                   self.transform.position[1])


@desper.event_handler(ON_WIN_EVENT)
class QuitOnWin:
    """On win, simply quit the game."""

    def on_win(self):
        desper.quit_loop()


@desper.event_handler(ON_WIN_EVENT)
class NextOnWin:
    """On win, raise exception to get to next level."""

    def on_win(self):
        raise Next()


class Next(Exception):
    """Custom exception to switch to the next level."""
    pass
