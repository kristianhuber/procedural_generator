import random

from world.biome.biome import biome_from
from world.noise_utils import HEIGHT_NOISE, BIOME_NOISE, NoiseGenerator, normalize


SIZE = 128
SEAM = 8
SIZE_AND_SEAMS = SIZE + 2 * SEAM

_EROSION_OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
_EROSION_CONSTANT = 0.1
_SEDIMENTATION_CONSTANT = 0.1
_WATER_CARRY_CAPACTIY_CONSTANT = 1.5

class Chunk:

    def __init__(self, worldX: int, worldY: int, seed: int):
        """
        Initializes a chunk.

        Args:
            worldX - The left most coordinate of the chunk in the world (excluding seem).
            worldY - The top most coorindate of the chunk in the world (excluding seem).
            seed - The seed used to generate this chunk.
        """
        self.worldX = worldX
        self.worldY = worldY
        self.seed = seed

        self.moisture_map = self._generate_grid_with_perlin_noise(BIOME_NOISE, False, 1)
        self.tempurature_map = self._generate_grid_with_perlin_noise(BIOME_NOISE, False, 2)

        self.biome_map = self._generate_biome_map()

        self.height_map = self._generate_height_map()

    def _generate_height_map(self) -> list[list]:
        return self._generate_grid_with_perlin_noise(HEIGHT_NOISE, True)

    def _generate_biome_map(self) -> list[list]:
        grid = self._generate_empty_grid()

        for chunkX in range(SIZE_AND_SEAMS):
            for chunkY in range(SIZE_AND_SEAMS):
                grid[chunkX][chunkY] = biome_from(self.moisture_map[chunkX][chunkY], self.tempurature_map[chunkX][chunkY])

        return grid

    def _generate_grid_with_perlin_noise(self, noise: NoiseGenerator, normalize_height: bool=False, seed_offset: int=0) -> list[list]:
        """Creates a grid filled with perlin noise that is the size of the chunk + seams."""
        grid = self._generate_empty_grid()

        for chunkX in range(SIZE_AND_SEAMS):
            for chunkY in range(SIZE_AND_SEAMS):
                raw_height  = noise.generate_noise(self.worldX + chunkX, self.worldY + chunkY, self.seed + seed_offset)

                grid[chunkX][chunkY] = normalize(raw_height) if normalize_height else raw_height

        return grid

    def _generate_empty_grid(self) -> list[list]:
        """Initializes an empty grid that is the size of the chunk + seams."""
        return [[0] * SIZE_AND_SEAMS for _ in range(SIZE_AND_SEAMS)]
    
    def _simulate_hydraulic_erosion(self, iterations: int=5000) -> None:
        """
        Simulates hydraulic erosion on this chunk.

        Args:
            iterations - number of rain drop iterations.
        """
        for _ in range(iterations):

            # Step 1: Pick a random starting location in the chunk.
            currentX = random.randint(0, SIZE_AND_SEAMS - 1)
            currentY = random.randint(0, SIZE_AND_SEAMS - 1)

            sediment = 0

            # The rain drop's journey.
            for _ in range(1000):

                current_h = self.height_map[currentX][currentY]

                # Step 2: Find the lowest neighbor.
                lowest_hx, lowest_hy = currentX, currentY
                lowest_h = current_h

                for offsetX, offsetY in _EROSION_OFFSETS:
                    neighborX, neighborY = currentX + offsetX, currentY + offsetY

                    # Check boundary conditions.
                    if 0 <= neighborX < SIZE_AND_SEAMS and 0 <= neighborY < SIZE_AND_SEAMS:
                        h = self.height_map[neighborX][neighborY]
                        if h <= lowest_h:
                            lowest_hx, lowest_hy, lowest_h = neighborX, neighborY, h
    
                # Step 3: Erosion and Sedimentation Logic

                # Drop all sediment if the original point is the lowest.
                if lowest_hx == currentX and lowest_hy == currentY:
                    self.height_map[lowest_hx][lowest_hy] += sediment
                    break
                
                # Determine the current carrying capacity.
                # The rain drop can carry more sediment when the slope is steeper and it has more energy.
                slope = current_h - lowest_h
                capacity = max(0, slope * _WATER_CARRY_CAPACTIY_CONSTANT)

                # Determine if this drop should deposit or erode.
                material_to_move = sediment - capacity

                if material_to_move > 0:
                    # Deposit sediment.
                    deposit_amount = material_to_move * _SEDIMENTATION_CONSTANT
                    deposit_amount = min(deposit_amount, material_to_move)
                    self.height_map[currentX][currentY] += deposit_amount
                    sediment -= deposit_amount
                else:
                    # Erode new material.
                    erosion_amount = -material_to_move * _EROSION_CONSTANT
                    self.height_map[currentX][currentY] -= erosion_amount
                    sediment += erosion_amount

                # Step 4: Update the current position and continue the loop.
                currentX, currentY = lowest_hx, lowest_hy

    def simulate_wind_erosion(self, iterations: int=5000):
        """
        Simulates wind erosion on this chunk.

        Args:
            iterations - number of wind gust iterations.
        """
        raise NotImplementedError

    def get_height_at(self, chunkX, chunkY) -> int:
        """
        Returns the height value at the coordinate.

        Args:
            chunkX - x coordinate within the chunk.
            chunkY - y coordinate within the chunk.
        """
        return self.height_map[SEAM + chunkX][SEAM + chunkY]
    
    def get_biome_at(self, chunkX, chunkY) -> int:
        """
        Returns the height value at the coordinate.

        Args:
            chunkX - x coordinate within the chunk.
            chunkY - y coordinate within the chunk.
        """
        return self.biome_map[SEAM + chunkX][SEAM + chunkY]
    