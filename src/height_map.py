import noise
import random

SIZE = 512

# Controls the "zoom" or feature size of the noise. A smaller scale produces smoother terrain, while a larger scale makes it more detailed and jagged.
SCALE = 100.0

# The number of layers of noise to combine. More octaves add more high-frequency detail.
OCTAVES = 6

# How much each additional octave contributes to the final noise. Higher values make the terrain rougher.
PERSISTENCE = 0.5

# How much the frequency changes per octave. A value of 2.0 means each octave is twice as detailed as the last.
LACUNNARITY = 2.0

class HeightMap:

    def __init__(self):
        self.world = [[0] * SIZE for _ in range(SIZE)]
        self.seed = random.randint(0, 1024)

    def generate_map(self):
        for i in range(SIZE):
            for j in range(SIZE):
                raw_height  = noise.pnoise2(
                                    i / SCALE,
                                    j / SCALE,
                                    octaves=OCTAVES,
                                    persistence=PERSISTENCE,
                                    lacunarity=LACUNNARITY,
                                    base=self.seed
                                )
                self.world[i][j] = self.normalize(raw_height)
                 
    def normalize(self, val):
        max_val = 255
        min_val = 0
        return (val + 1) * (max_val - min_val) / 2
