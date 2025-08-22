import noise


class NoiseGenerator:

    def __init__(self, scale=300.0, octaves=6, persistence=0.5, lacunarity=2.0):
        """
        Holds parameters for generating perlin noise.

        Args:
            scale -  Controls the "zoom" or feature size of the noise. A smaller scale produces smoother terrain, while a larger scale makes it more detailed and jagged.
            octaves - The number of layers of noise to combine. More octaves add more high-frequency detail.
            persistence - How much each additional octave contributes to the final noise. Higher values make the terrain rougher.
            lacunarity - How much the frequency changes per octave. A value of 2.0 means each octave is twice as detailed as the last.
        """
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

    def generate_noise(self, worldX: int, worldY: int, seed: int) -> float:
        """
        Generates a noise value between -1 and 1, based on the parameters.

        Args:
            worldX - x coordinate in the world.
            worldY - y coordinate in the world.
            seed - the world's seed.
        """
        return noise.snoise2(
            worldX / self.scale,
            worldY / self.scale,
            octaves=self.octaves,
            persistence=self.persistence,
            lacunarity=self.lacunarity,
            base=seed
        )


STANDARD_NOISE = NoiseGenerator()


def normalize(v, min=0, max=255) -> int:
    """
    Takes a value between -1 and 1 and transforms it into a number between a min and max value.

    Args:
        v - The value to be normalized.
        min - The minimum normalized value.
        max - The maximum normalized value.
    """
    return (max - min) * ((v + 1) / 2) + min