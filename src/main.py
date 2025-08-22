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

dragging = False
posX, posY = 0, 0

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                dx, dy = event.rel
                posX += dx
                posY += dy

    screen.fill((0, 0, 0))
    render_world(screen, posX, posY, my_world)
    pygame.display.flip()

# Quit Pygame
pygame.quit()