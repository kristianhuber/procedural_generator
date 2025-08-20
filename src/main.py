import pygame
from height_map import HeightMap

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Procedural Terrain Generator")

heightMap = HeightMap()
heightMap.generate_map()

# --- Draw the map ---
for j in range(len(heightMap.world)):
    for i in range(len(heightMap.world[j])):
        # Use the correct syntax to access the map data
        height_val = heightMap.world[j][i]
        
        # Create a grayscale color tuple
        c = (height_val, height_val, height_val)

        # Draw the pixel at the original coordinates (no scaling needed)
        screen.set_at((i, j), c)

# Update the display
pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()