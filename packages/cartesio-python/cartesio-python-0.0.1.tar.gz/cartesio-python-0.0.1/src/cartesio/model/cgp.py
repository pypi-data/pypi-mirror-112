from cartesio.model.ea.ga import ObservableGeneticAlgorithm
from cartesio.model.ea.decoder import Decoder, EndpointedDecoder

from abc import ABC, abstractmethod
from typing import List


class AbstractModel(ABC):
    @abstractmethod
    def fit(self,
            train_x: List,
            train_y: List,
            n_populations: int,
            n_individuals: int,
            generations: int,
            callbacks: List = []):
        pass

    @abstractmethod
    def evaluate(self, test_x: List, test_y: List):
        pass

    @abstractmethod
    def predict(self, x: List):
        pass


class AbstractCGP(AbstractModel, ABC):
    def __init__(self, decoder):
        self.decoder = decoder
        self.genetic_algorithm = ObservableGeneticAlgorithm(decoder)
        self._compose_genetic_algorithm()

    def add_callback(self, callback):
        self.genetic_algorithm.attach(callback)

    @abstractmethod
    def _compose_genetic_algorithm(self):
        pass

    def fit(self, x, y, generations, populations, individuals, callbacks=[]):
        self.genetic_algorithm.clear()
        for callback in callbacks:
            self.genetic_algorithm.attach(callback)
        history = self.genetic_algorithm.run(x, y, generations, populations, individuals)
        elite = history.get_best(generations-1)
        return elite, history

    def evaluate(self, y, p):
        return self.genetic_algorithm.evaluate_one_individual(y, p)

    def predict(self, x, individual):
        p, t = self.decoder.decode(individual, x)
        return p


class StandardCGP(AbstractCGP):
    def __init__(self, metadata, function_set):
        decoder = Decoder(metadata, function_set)
        super(StandardCGP, self).__init__(decoder)


class EndpointedCGP(AbstractCGP):
    def __init__(self, metadata, function_set, endpoint):
        decoder = EndpointedDecoder(metadata, function_set, endpoint)
        super(EndpointedCGP, self).__init__(decoder)
