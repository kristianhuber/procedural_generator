
class Biome:
    def __init__(self, biome_color: tuple[int, int, int]):
        self.biome_color = biome_color

TUNDRA = Biome((0, 0, 55))
TAIGA = Biome((0, 0, 155))
GRASSLAND = Biome((0, 255, 0))
FOREST = Biome((0, 150, 0))
SWAMP = Biome((0, 55, 0))
DESERT = Biome((255, 0, 0))
SAVANNAH = Biome((155, 0, 0))
JUNGLE = Biome((55, 0, 0))


def biome_from(moisture: float, tempurature: float) -> Biome:
    if tempurature <= -0.33333:
        # Cold
        if moisture <= 0:
            return TUNDRA
        else:
            return TAIGA
    elif tempurature <= 0.33333:
        # Temperate
        if moisture <= -0.33333:
            return GRASSLAND
        elif moisture <= 0.33333:
            return FOREST
        else:
            return SWAMP
    else:
        # Hot
        if moisture <= -0.33333:
            return DESERT
        elif moisture <= 0.33333:
            return SAVANNAH
        else:
            return JUNGLE