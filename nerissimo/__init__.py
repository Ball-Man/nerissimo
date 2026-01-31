import sys
import pathlib
from functools import partial
from collections import deque

import desper
import sdl2
from sdl2 import sdlttf as ttf

from . import graphics
from . import desktop
from . import game
from . import levels

try:
    from . import bonnet
except Exception:
    pass

window = None

# Layout and spacing
LAYOUT_START_X = 32
LAYOUT_START_Y = 0
LAYOUT_X_CELL_OFFSET = 1
LAYOUT_Y_CELL_OFFSET = 1


def start_game(on_bonnet: bool = False, window_scale: int = 1):
    from .log import logger
    logger.info('window scale %d', window_scale)
    sdl2.SDL_Init(0)
    ttf.TTF_Init()

    if not on_bonnet:       # Only create a window on desktop
        global window
        window = sdl2.SDL_CreateWindow(b'Nerissimo',
                                       sdl2.SDL_WINDOWPOS_UNDEFINED,
                                       sdl2.SDL_WINDOWPOS_UNDEFINED,
                                       graphics.BONNET_WIDTH * window_scale,
                                       graphics.BONNET_HEIGHT * window_scale,
                                       0)

    if getattr(sys, 'frozen', False):
        resource_root = pathlib.Path(sys.executable).absolute().parent
        logger.info('Game frozen, executable path is %s', resource_root)
    else:
        resource_root = pathlib.Path(__file__).absolute().parents[1]

    directory_populator = desper.DirectoryResourcePopulator(
        resource_root / 'resources',
        trim_extensions=True)

    directory_populator.add_rule('sprites', graphics.SurfaceHandle)
    directory_populator.add_rule('fonts', graphics.TTFHandle)
    directory_populator(desper.resource_map)

    for level_name, level_transformer in levels.transformer_list:
        resource_key = f'worlds/{level_name}'
        desper.resource_map[resource_key] = desper.WorldHandle()
        desper.resource_map.get(resource_key).transform_functions.append(level_transformer)

    platform_specific_transformer = desktop.game_world_transformer
    if on_bonnet:
        platform_specific_transformer = bonnet.game_world_transformer

    # Platform specific world transformer
    for world_handle in desper.resource_map['worlds'].handles.values():
        world_handle.transform_functions.append(platform_specific_transformer)

    desper.default_loop.switch(desper.resource_map.get(f'worlds/{levels.transformer_list[0][0]}'))
    level_queue = deque(map(lambda pair: pair[0], levels.transformer_list))
    try:
        while True:
            try:
                desper.default_loop.loop()
            except game.Next:
                level_queue.rotate()
                desper.default_loop.switch(desper.resource_map.get(f'worlds/{level_queue[0]}'),
                                           clear_current=True)
    except desper.Quit:
        pass

    if not on_bonnet:       # Window exists on desktop only
        sdl2.SDL_DestroyWindow(window)

    sdl2.SDL_Quit()
