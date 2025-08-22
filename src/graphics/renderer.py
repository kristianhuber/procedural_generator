import pygame

from pygame import Surface
from world.chunk import Chunk, SIZE
from world.world import World

def _colorize(height):
    return (height, height, height)

def render_chunk(screen: Surface, chunk: Chunk):
    for x in range(SIZE):
        for y in range(SIZE):
            h = chunk.get_height_at(x, y)
            
            pixel_color = _colorize(h)

            screen.set_at((chunk.worldX + x, chunk.worldY + y), pixel_color)

    pygame.display.flip()

def render_world(screen: Surface, world: World):
    for chunk in world.chunks:
        render_chunk(screen, chunk)