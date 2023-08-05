# from cartesio.model.ea.population import Population, PopulationWithElite
from abc import ABC, abstractmethod  # Abstract Base Classes


class EvolutionStrategy(ABC):
    @abstractmethod
    def selection(self, population):
        pass

    @abstractmethod
    def reproduction(self, population):
        pass


class OnePlusLambda(EvolutionStrategy):
    def __init__(self):
        self.mu = 1

    def selection(self, population):
        new_elite, fitness = population.get_best_individual()
        population.set_elite(new_elite)

    def reproduction(self, population):
        elite = population.get_elite()
        for i in range(self.mu, population.n):
            population.set_individual(i, elite.clone())
