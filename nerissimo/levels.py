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
                                                           graphics.BONNET_WIDTH)), 99)

    world.create_entity(game.NextOnWin())
    world.create_entity(game.QuitOnKey(sdl2.SDL_SCANCODE_ESCAPE))


def base_square_level_transformer(handle: desper.WorldHandle,
                                  world: desper.World):
    """First screen, move the square."""
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
    """Title drop."""
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


def base_crossing_level_transformer(handle: desper.WorldHandle,
                                    world: desper.World):
    """Oscillating blocks leave a hole."""
    world.create_entity(
        desper.Transform2D(position=(2, 2)),
        *graphics.prepare_surface_array_components(graphics.build_surface(20, 20, 0xFF)),
        game.Velocity(0, 0),
        game.UserControlled(),
        graphics.EnsureClipped())

    world.create_entity(
        desper.Transform2D(position=(22, 49)),
        *graphics.prepare_surface_array_components(graphics.build_surface(40, 20, 0xFF)),
        game.Oscillate(20, 4))

    world.create_entity(
        desper.Transform2D(position=(22, 49)),
        *graphics.prepare_surface_array_components(graphics.build_surface(20, 20, 0xFF)))

    world.add_processor(desper.OnUpdateProcessor())


def base_crossing2_level_transformer(handle: desper.WorldHandle,
                                     world: desper.World):
    """Oscillating blocks leave a hole., double oscillation"""
    world.create_entity(
        desper.Transform2D(position=(2, 2)),
        *graphics.prepare_surface_array_components(graphics.build_surface(20, 20, 0xFF)),
        game.Velocity(0, 0),
        game.UserControlled(),
        graphics.EnsureClipped())

    world.create_entity(
        desper.Transform2D(position=(22, 49)),
        *graphics.prepare_surface_array_components(graphics.build_surface(40, 20, 0xFF)),
        game.Oscillate(20, 2.3))

    world.create_entity(
        desper.Transform2D(position=(22, 49)),
        *graphics.prepare_surface_array_components(graphics.build_surface(20, 20, 0xFF)),
        game.Oscillate(-20, 2.3))

    world.add_processor(desper.OnUpdateProcessor())


def base_knight_level_transformer(handle: desper.WorldHandle,
                                  world: desper.World):
    """Knight movement to eat a standing knight."""
    world.create_entity(
        desper.Transform2D(position=(32, 12)),
        *graphics.prepare_surface_array_components(desper.resource_map['sprites/knight']),
        game.Velocity(0, 0),
        game.UserControlledKnight((0, 0, graphics.BONNET_HEIGHT, graphics.BONNET_WIDTH)),
        graphics.EnsureClipped())

    world.create_entity(
        desper.Transform2D(position=(22, 92)),
        *graphics.prepare_surface_array_components(desper.resource_map['sprites/knight']))

    world.add_processor(game.TargetProcessor())
    world.add_processor(desper.OnUpdateProcessor())


transformer_list = [
    ('square', base_square_level_transformer),
    ('nerissimo', base_nerissimo_level_transformer),
    ('crossing', base_crossing_level_transformer),
    ('knight', base_knight_level_transformer),
]
