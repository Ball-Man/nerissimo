import desper
import sdl2
from sdl2 import sdlttf as ttf

from . import graphics
from . import game
from .log import logger


def base_level_transformer(handle: desper.WorldHandle,
                           world: desper.World,
                           framerate: float = 1 / 30):
    """Common to all levels."""
    world.add_processor(desper.CoroutineProcessor())
    world.add_processor(graphics.TimeProcessor())

    # Setup screen rendering
    world.create_entity(graphics.ScreenSurfaceHandler())
    screen_surface, screen_surface_array = graphics.prepare_surface_array_components(
            sdl2.SDL_CreateRGBSurfaceWithFormat(0, graphics.BONNET_WIDTH,
                                                graphics.BONNET_HEIGHT, 1,
                                                sdl2.SDL_PIXELFORMAT_RGB332))
    world.create_entity(
        graphics.ScreenSurface(), screen_surface, screen_surface_array)

    world.add_processor(graphics.TimeProcessor(framerate))
    world.add_processor(game.VelocityProcessor())
    world.add_processor(game.WinConditionProcessor(screen_surface_array), 1000)
    world.add_processor(graphics.ClipTransformsProcessors((0, 0, graphics.BONNET_HEIGHT,
                                                           graphics.BONNET_WIDTH)))

    world.create_entity(game.NextOnWin())


def base_square_level_transformer(handle: desper.WorldHandle,
                                  world: desper.World):
    """Instantiate game world basics (common to all platforms)."""
    world.create_entity(
        desper.Transform2D(position=(2, 2)),
        *graphics.prepare_surface_array_components(graphics.build_surface(30, 30, 0xFF)),
        game.Velocity(0, 0),
        game.UserControlled(),
        graphics.EnsureClipped())

    world.create_entity(
        desper.Transform2D(position=(17, 49)),
        *graphics.prepare_surface_array_components(graphics.build_surface(30, 30, 0xFF)))


def base_nerissimo_level_transformer(handle: desper.WorldHandle,
                                     world: desper.World):
    """Instantiate game world basics (common to all platforms)."""
    nerissimo = graphics.render_text('fonts/exepixelperfect', 'NERISSIMO')

    world.create_entity(
        desper.Transform2D(position=(2, 2)),
        *graphics.prepare_surface_array_components(nerissimo),
        game.Velocity(0, 0),
        game.UserControlled(),
        graphics.EnsureClipped())

    world.create_entity(
        desper.Transform2D(position=(20, 2)),
        *graphics.prepare_surface_array_components(nerissimo))


transformer_list = [
    ('square', base_square_level_transformer),
    ('square2', base_nerissimo_level_transformer),
]
