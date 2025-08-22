from world.noise_utils import STANDARD_NOISE, normalize


SIZE = 128
SEAM = 8
SIZE_AND_SEAMS = SIZE + 2 * SEAM


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
        self.grid = self._generate_grid_with_perlin_noise()

    def _generate_grid_with_perlin_noise(self) -> list[list]:
        """Creates a grid filled with perlin noise that is the size of the chunk + seams."""
        empty_grid = self._generate_empty_grid()

        for chunkX in range(SIZE_AND_SEAMS):
            for chunkY in range(SIZE_AND_SEAMS):
                raw_height  = STANDARD_NOISE.generate_noise(self.worldX + chunkX, self.worldY + chunkY, self.seed)

                empty_grid[chunkY][chunkX] = normalize(raw_height)

        return empty_grid

    def _generate_empty_grid(self) -> list[list]:
        """Initializes an empty grid that is the size of the chunk + seams."""
        return [[0] * SIZE_AND_SEAMS for _ in range(SIZE_AND_SEAMS)]
    
    def get_height_at(self, chunkX, chunkY) -> int:
        """
        Returns the height value at the coordinate.

        Args:
            chunkX - x coordinate within the chunk.
            chunkY - y coordinate within the chunk.
        """
        return self.grid[SEAM + chunkY][SEAM + chunkX]
    