
from cartesio.model.cgp import StandardCGP
from cartesio.cv.opencv_set import OPENCV_SET
from cartesio.mutations import MutationAllRandom, MutationClassic
from cartesio.model.ea.strategy import OnePlusLambda
from cartesio.model.ea.fitness import FitnessIOU
from cartesio.model.ea.genome import GenomeFactory


# Cartesian Genetic Programming for Image Processing
class CGPIP(StandardCGP):
    def __init__(self, metadata, mutation_rate, output_mutation_rate):
        self.mutation_rate = mutation_rate
        self.output_mutation_rate = output_mutation_rate
        super().__init__(metadata, OPENCV_SET)

    def _compose_genetic_algorithm(self):
        self.genetic_algorithm.set_initialization(MutationAllRandom(self.decoder._m, self.decoder.function_set.n_functions), GenomeFactory(self.decoder._m.prototype))
        self.genetic_algorithm.set_mutation(MutationClassic(self.decoder._m, self.decoder.function_set.n_functions, self.mutation_rate, self.output_mutation_rate))
        self.genetic_algorithm.set_evolution_strategy(OnePlusLambda())
        self.genetic_algorithm.set_fitness(FitnessIOU())
