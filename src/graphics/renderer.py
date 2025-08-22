from pygame import Surface
from world.chunk import Chunk, SIZE
from world.world import World

def _grayscale(height):
    return (height, height, height)

def _colorize(height):
    if height < 125:
        return (0, 125, 200)

    if height > 175:
        return (height - 50, height - 50, height - 50)

    return (0, height - 50, 0)

def render_chunk(screen: Surface, chunk: Chunk):
    for x in range(SIZE):
        for y in range(SIZE):
            h = chunk.get_height_at(x, y)
            
            pixel_color = _colorize(h)

            screen.set_at((chunk.worldX + x, chunk.worldY + y), pixel_color)

def render_world(screen: Surface, world: World):
    for chunk in world.chunks:
        render_chunk(screen, chunk)