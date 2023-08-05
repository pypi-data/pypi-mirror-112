import numpy as np
from cartesio.model.ea.individual import Individual
from abc import ABC, abstractmethod  # Abstract Base Classes


class Population(ABC):
    def __init__(self, n):
        self.n = n
        self.__individuals = [None] * (self.n)
        self.fitness = {'fitness': np.zeros(self.n), 'time': np.zeros(self.n)}

    def set_individual(self, idx, individual):
        self.__individuals[idx] = individual

    def get_individual(self, idx):
        return self.__individuals[idx]

    def get_individuals(self):
        return self.__individuals

    @abstractmethod
    def get_best_individual(self):
        pass


class PopulationWithElite(Population):
    def __init__(self, p_lambda):
        super().__init__(1 + p_lambda)

    def set_elite(self, individual: Individual):
        self.set_individual(0, individual)

    def get_elite(self):
        return self.get_individual(0)

    def get_best_individual(self):
        scores = list(zip(self.fitness['fitness'], self.fitness['time']))
        individuals = np.array(scores, dtype=[('fitness', float), ('time', float)])

        # get the first element to minimize
        best_fitness_idx = np.argsort(individuals)[0]
        best_individual = self.get_individual(best_fitness_idx)
        return best_individual, self.fitness['fitness'][best_fitness_idx]
