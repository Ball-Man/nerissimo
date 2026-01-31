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
                                   velocity.value * (dt, dt))


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


@desper.event_handler(ON_WIN_EVENT)
class QuitOnWin:
    """On win, simply quit the game."""

    def on_win(self):
        desper.quit_loop()
