import random

from world.chunk import Chunk, SIZE

class World:

    def __init__(self, seed: int = 0):
        self.seed = random.randint(0, 2048) if seed == 0 else seed
        self.chunks = []

        for i in range(4):
            for j in range(4):
                self.chunks.append(Chunk(i * SIZE, j * SIZE, self.seed))