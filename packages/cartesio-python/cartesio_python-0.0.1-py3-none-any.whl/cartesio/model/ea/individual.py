
from cartesio.model.ea.genome import Genome


class Individual(object):
    def __init__(self):
        self.G = None
        self.fitness = 0.
        self.time = 0.

    def set_genome(self, G: Genome):
        self.G = G


class IndividualMultiGenome(object):
    def __init__(self):
        self.Gs = []
        self.fitness = 0.
        self.time = 0.

    def add_genome(self, G: Genome):
        self.Gs.append(G)
