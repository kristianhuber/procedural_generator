import pygame

from graphics.renderer import render_world
from world.world import World

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Procedural Terrain Generator")

# Generate the world
my_world = World()

# Render the world
render_world(screen, my_world)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()