
import numpy as np


class IndividualHistory(object):
    def __init__(self):
        self.fitness = {'fitness': 0., 'time': 0.}
        self.sequence = None

    def set_sequence(self, sequence):
        self.sequence = sequence

    def set_values(self, sequence, fitness, time):
        self.sequence = sequence
        self.fitness['fitness'] = fitness
        self.fitness['time'] = time


class PopulationHistory(object):
    def __init__(self, n_individuals):
        self.individuals = {}
        for i in range(n_individuals+1):
            self.individuals[i] = IndividualHistory()

    def set_population(self, individuals, fitness, times):
        for i in range(len(individuals)):
            self.individuals[i].set_values(individuals[i].sequence, fitness[i], times[i])

    def get_best_fitness(self):
        return self.individuals[0].fitness['fitness'], self.individuals[0].fitness['time']

    def get_individuals(self):
        return self.individuals.items()


class GenerationHistory(object):
    def __init__(self, n, n_populations, n_individuals):
        self.n = n
        self.populations = {}
        for i in range(n_populations):
            self.populations[i] = PopulationHistory(n_individuals)

    def set_population(self, population, individuals, fitness, times):
        self.populations[population].set_population(individuals, fitness, times)

    def get_best(self):
        fitnesses = []
        times = []
        individuals = []
        for i, p in self.populations.items():
            f, t = p.get_best_fitness()
            fitnesses.append(f)
            times.append(t)
            individuals.append(p)
        values = list(zip(fitnesses, times))
        individuals = np.array(values, dtype=[('fitness', float), ('time', float)])
        best_fitness_idx = np.argsort(individuals)[0]

        best_individual = self.populations[best_fitness_idx].individuals[0]
        return best_individual, fitnesses[best_fitness_idx]


class GenerationSinglePopHistory(object):
    def __init__(self, n, n_individuals):
        self.n = n
        self.population = PopulationHistory(n_individuals)

    def set_population(self, population, individuals, fitness, times):
        self.population.set_population(individuals, fitness, times)

    def get_populations(self):
        return {0: self.population}.items()

    def get_best(self):
        return self.population.individuals[0]


class TrainingHistory(object):
    def __init__(self, n_generations, n_populations, n_individuals):
        self.generations = {}
        if n_populations == 1:
            self.generations['first'] = GenerationSinglePopHistory('first', n_individuals)
            for i in range(n_generations):
                self.generations[i] = GenerationSinglePopHistory(i, n_individuals)
        else:
            self.generations['first'] = GenerationHistory('first', n_populations, n_individuals)
            for i in range(n_generations):
                self.generations[i] = GenerationHistory(i, n_populations, n_individuals)

    def set_population(self, generation, population, individuals, fitness, times):
        self.generations[generation].set_population(population, individuals, fitness, times)

    def get_best(self, generation):
        return self.generations[generation].get_best()
