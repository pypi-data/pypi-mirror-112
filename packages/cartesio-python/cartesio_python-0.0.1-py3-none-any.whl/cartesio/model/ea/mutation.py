from abc import ABC, abstractmethod  # Abstract Base Classes

import numpy as np
from cartesio.model.ea.genome import Genome, GenomeMetadata, GenomeReaderWriter
import random


class Mutation(GenomeReaderWriter, ABC):
    def __init__(self, metadata, n_functions):
        super(Mutation, self).__init__(metadata)
        self.n_functions = n_functions
        self.parameter_max_value = 256

    def random_parameters(self):
        return np.random.randint(self.parameter_max_value, size=self._m.n_parameters)

    def random_functions(self):
        return np.random.randint(self.n_functions)

    def random_connections(self, idx_connections: int, n_connections: int = 1):
        return np.random.randint(idx_connections, size=n_connections)

    def mutate_function(self, G: Genome, idx: int):
        self.write_function(G, idx, self.random_functions())

    def mutate_connections(self, G: Genome, idx: int, only_one: int = None):
        new_connections = self.random_connections(self._m.gen_idx+idx, self._m.n_connections)
        if only_one is not None:
            new_value = new_connections[only_one]
            new_connections = self.read_connections(G, idx)
            new_connections[only_one] = new_value
        self.write_connections(G, idx, new_connections)

    def mutate_parameters(self, G: Genome, idx: int, only_one: int = None):
        new_parameters = self.random_parameters()
        if only_one is not None:
            old_parameters = self.read_parameters(G, idx)
            old_parameters[only_one] = new_parameters[only_one]
            new_parameters = old_parameters.copy()
        self.write_parameters(G, idx, new_parameters)

    def mutate_output(self, G: Genome, idx: int):
        new_connection = self.random_connections(self._m.out_idx, 1)  # only 1 connection for output
        self.write_output_connection(G, idx, new_connection)

    @abstractmethod
    def mutate(self, G: Genome):
        pass


class MutationClassic(Mutation):
    def __init__(self, metadata, n_functions, mutation_rate, output_mutation_rate):
        super().__init__(metadata, n_functions)
        self.mutation_rate = mutation_rate
        self.output_mutation_rate = output_mutation_rate
        self.init()

    def init(self):
        self.n_mutations = int(np.floor(self._m.n_genes * self._m.gene_length * self.mutation_rate))
        self.all_indices = np.indices((self._m.n_genes, self._m.gene_length))
        self.all_indices = np.vstack((self.all_indices[0].ravel(), self.all_indices[1].ravel())).T
        self.sampling_range = range(len(self.all_indices))

    def mutate(self, G):
        sampling_indices = np.random.choice(self.sampling_range, self.n_mutations, replace=False)
        sampling_indices = self.all_indices[sampling_indices]

        for idx, mutation_parameter_index in sampling_indices:
            if mutation_parameter_index == 0:
                self.mutate_function(G, idx)
            elif mutation_parameter_index <= self._m.n_connections:
                connection_idx = mutation_parameter_index-1
                self.mutate_connections(G, idx, only_one=connection_idx)
            else:
                parameter_idx = mutation_parameter_index - self._m.n_connections - 1
                self.mutate_parameters(G, idx, only_one=parameter_idx)
        for output in range(self._m.n_outputs):
            if random.random() < self.output_mutation_rate:
                self.mutate_output(G, output)
        return G


class MutationAllRandom(Mutation):
    '''
    Can be used to initialize genome (G) randomly
    '''
    def __init__(self, metadata: GenomeMetadata, n_functions: int):
        super().__init__(metadata, n_functions)

    def mutate(self, G: Genome):
        # mutate genes
        for i in range(self._m.n_genes):
            self.mutate_function(G, i)
            self.mutate_connections(G, i)
            self.mutate_parameters(G, i)
        # mutate outputs
        for i in range(self._m.n_outputs):
            self.mutate_output(G, i)
        return G
