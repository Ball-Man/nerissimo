import pathlib
from functools import partial

import desper
import sdl2

from . import graphics
from . import desktop
# from . import game

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


def base_game_world_transformer(handle: desper.WorldHandle,
                                world: desper.World):
    """Instantiate game world basics (common to all platforms)."""
    world.add_processor(desper.CoroutineProcessor())
    world.add_processor(graphics.TimeProcessor())

    # Setup screen rendering
    world.create_entity(graphics.ScreenSurfaceHandler())
    world.create_entity(
        graphics.ScreenSurface(),
        sdl2.SDL_CreateRGBSurfaceWithFormat(0, graphics.BONNET_WIDTH,
                                            graphics.BONNET_HEIGHT, 1,
                                            sdl2.SDL_PIXELFORMAT_RGB332))


def start_game(on_bonnet: bool = False, window_scale: int = 1):
    sdl2.SDL_Init(0)

    if not on_bonnet:       # Only create a window on desktop
        global window
        window = sdl2.SDL_CreateWindow(b'Nerissimo',
                                       sdl2.SDL_WINDOWPOS_UNDEFINED,
                                       sdl2.SDL_WINDOWPOS_UNDEFINED,
                                       graphics.BONNET_WIDTH * window_scale,
                                       graphics.BONNET_HEIGHT * window_scale,
                                       0)

    directory_populator = desper.DirectoryResourcePopulator(
        pathlib.Path(__file__).absolute().parents[1] / 'resources',
        trim_extensions=True)

    directory_populator.add_rule('sprites', graphics.SurfaceHandle)
    directory_populator(desper.resource_map)

    desper.resource_map['worlds/game'] = desper.WorldHandle()
    desper.resource_map.get('worlds/game').transform_functions.append(
        partial(base_game_world_transformer))

    # Platform specific world transformer
    platform_specific_transformer = desktop.game_world_transformer
    if on_bonnet:
        platform_specific_transformer = bonnet.game_world_transformer

    desper.resource_map.get('worlds/game').transform_functions.append(
            platform_specific_transformer)

    desper.default_loop.switch(desper.resource_map.get('worlds/game'))
    try:
        desper.default_loop.loop()
    except desper.Quit:
        pass

    if not on_bonnet:       # Window exists on desktop only
        sdl2.SDL_DestroyWindow(window)

    sdl2.SDL_Quit()
