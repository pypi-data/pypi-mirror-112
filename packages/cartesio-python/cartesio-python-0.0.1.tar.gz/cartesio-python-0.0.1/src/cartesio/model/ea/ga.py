
from cartesio.model.ea.population import PopulationWithElite
from cartesio.helpers.observer import Observable
from cartesio.training.history import TrainingHistory


class Initialization(object):
    def __init__(self, initialization_function, factory):
        self.factory = factory
        self.initialization = initialization_function

    def do(self, ga):
        for p in range(ga.n_pop):
            population = PopulationWithElite(ga.n_ind)
            for i in range(population.n):
                individual = self.initialization.mutate(self.factory.create())
                population.set_individual(i, individual)
            ga.populations.append(population)


class Evaluation(object):
    def __init__(self, decoder, fitness):
        self.decoder = decoder
        self.fitness = fitness

    def __evaluate_population(self, population, ga):
        fitnesses = []
        times = []
        individuals = population.get_individuals()
        y_pred = []
        for individual in individuals:
            pred, t = self.decoder.decode(individual, ga.x)
            y_pred.append(pred)
            times.append(t)
        fitnesses = self.fitness.evaluate(ga.y, y_pred)
        return fitnesses, times, individuals

    def do(self, ga, first=False):
        for p, population in enumerate(ga.populations):
            fitnesses, times, individuals = self.__evaluate_population(population, ga)
            population.fitness['fitness'] = fitnesses
            population.fitness['time'] = times
            if first:
                ga.history.set_population('first', p, individuals, fitnesses, times)
            else:
                ga.history.set_population(ga.current_generation, p, individuals, fitnesses, times)


class GeneticAlgorithm():
    def __init__(self, decoder):
        self.decoder = decoder
        self.history = None
        self.x = None
        self.y = None
        self.populations = []
        self.n_gen = None
        self.n_pop = None
        self.n_ind = None
        self.current_generation = 0

        # genetic altgorithm components
        self.initialization = None
        self.evolution_strategy = None
        self.mutation = None
        self.evaluation = None

    def set_initialization(self, init_function, factory):
        self.initialization = Initialization(init_function, factory)

    def set_fitness(self, fitness):
        self.evaluation = Evaluation(self.decoder, fitness)

    def set_evolution_strategy(self, evolution_strategy):
        self.evolution_strategy = evolution_strategy

    def set_mutation(self, mutation_function):
        self.mutation = mutation_function

    def selection(self):
        for p in range(self.n_pop):
            self.evolution_strategy.selection(self.populations[p])

    def reproduction(self):
        for p in range(self.n_pop):
            self.evolution_strategy.reproduction(self.populations[p])

    def mutate(self):
        for p in range(self.n_pop):
            for i in range(1, self.populations[p].n):
                individual = self.populations[p].get_individual(i)
                individual = self.mutation.mutate(individual)
                self.populations[p].set_individual(i, individual)

    def evaluate_one_individual(self, y, p):
        return self.evaluation.fitness.evaluate(y, p)

    def is_done(self):
        return self.current_generation >= self.n_gen

    def _build(self, x, y, generations, populations, individuals):
        self.history = TrainingHistory(generations, populations, individuals)
        self.x = x
        self.y = y
        self.populations = []
        self.n_gen = generations
        self.n_pop = populations
        self.n_ind = individuals
        self.current_generation = 0
        self.initialization.do(self)
        self.evaluation.do(self, first=True)

    def _loop(self):
        while not self.is_done():
            self._step()
            self.current_generation += 1

    def _step(self):
        self.selection()
        self.reproduction()
        self.mutate()
        self.evaluation.do(self)

    def run(self, x, y, generations, populations, individuals):
        # create populations and make first evaluation
        self._build(x, y, generations, populations, individuals)

        # genetic algorithm loop
        self._loop()

        return self.history


class ObservableGeneticAlgorithm(GeneticAlgorithm, Observable):
    def _step(self):
        super()._step()
        self.notify({'event': 'on_evaluation_end', 'generation': self.history.generations[self.current_generation]})
