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

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print("Loading new world...")
                my_world = World()
                
    screen.fill((0, 0, 0))
    render_world(screen, my_world)
    pygame.display.flip()

# Quit Pygame
pygame.quit()