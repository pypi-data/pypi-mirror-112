import numpy as np
import copy

from cartesio.helpers.factory import Factory, Prototype
from abc import ABC, abstractmethod
import ast


class GenomeMetadata(object):
    """Genome Metadata describes the Genome sequence

    Args:
        object ([type]): [description]
    """
    def __init__(self, n_inputs, n_genes, n_outputs, n_connections, n_parameters):
        self.sequence_length = n_inputs + n_genes + n_outputs
        self.gene_length = 1 + n_connections + n_parameters
        self.n_genes = n_genes
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_connections = n_connections
        self.n_parameters = n_parameters

        # define indices to short access
        # sequence indices
        self.in_idx = 0
        self.gen_idx = n_inputs
        self.out_idx = self.gen_idx + n_genes

        # gene indices
        self.func_idx = 0
        self.con_idx = 1
        self.para_idx = self.con_idx + n_connections

        self.prototype = Genome(shape=(self.sequence_length, self.gene_length))

    @classmethod
    def from_json(cls, json_data):
        return GenomeMetadata(
            json_data['n_in'],
            json_data['columns'],
            json_data['n_out'],
            json_data['n_conn'],
            json_data['n_para']
        )


class Genome(Prototype):
    """
    Only store "DNA" in a numpy array
    No metadata stored in DNA to avoid duplicates
    Avoiding RAM overload: https://refactoring.guru/design-patterns/flyweight
    Default genome would be: 3 inputs, 10 function nodes (2 connections and 2 parameters), 1 output,
    so with shape (14, 5)

    Args:
        Prototype ([type]): [description]

    Returns:
        [type]: [description]
    """

    def __init__(self, shape: tuple = (14, 5), sequence: np.ndarray = None):
        if sequence is not None:
            self.sequence = sequence
        else:
            self.sequence = np.zeros(shape=shape, dtype=np.uint8)

    def __copy__(self):
        new = self.__class__(*self.sequence.shape)
        new.__dict__.update(self.__dict__)
        return new

    def __deepcopy__(self, memo={}):
        new = self.__class__(*self.sequence.shape)
        new.sequence = self.sequence.copy()
        return new

    def clone(self):
        return copy.deepcopy(self)

    @classmethod
    def from_json(cls, json_data):
        data_as_ndarray = np.asarray(ast.literal_eval(json_data))
        G = Genome(sequence=data_as_ndarray)
        return G


class GenomeFactory(Factory):
    def __init__(self, genome_prototype: Genome):
        super().__init__(genome_prototype)


class GenomeAdapter(ABC):
    '''
    Adpater Design Pattern: https://refactoring.guru/design-patterns/adapter
    '''
    def __init__(self, metadata):
        self._m = metadata


class GenomeWriter(GenomeAdapter):
    def write_function(self, G, gene_idx, function_id):
        G.sequence[self._m.gen_idx+gene_idx, self._m.func_idx] = function_id

    def write_connections(self, G, gene_idx, connections):
        G.sequence[self._m.gen_idx+gene_idx, self._m.con_idx:self._m.para_idx] = connections

    def write_parameters(self, G, gene_idx, parameters):
        G.sequence[self._m.gen_idx+gene_idx, self._m.para_idx:] = parameters

    def write_output_connection(self, G, output_index, connection):
        G.sequence[self._m.out_idx+output_index, self._m.con_idx] = connection


class GenomeReader(GenomeAdapter):
    def read_sequence(self, G):
        return G.sequence

    def read_function(self, G, gene_idx):
        return G.sequence[self._m.gen_idx + gene_idx, self._m.func_idx]

    def read_connections(self, G, gene_idx):
        return G.sequence[self._m.gen_idx + gene_idx, self._m.con_idx:self._m.para_idx]

    def read_active_connections(self, G, gene_idx, active_connections):
        return G.sequence[self._m.gen_idx + gene_idx, self._m.con_idx:self._m.con_idx+active_connections]

    def read_parameters(self, G, gene_idx):
        return G.sequence[self._m.gen_idx + gene_idx, self._m.para_idx:]

    def read_outputs(self, G):
        return G.sequence[self._m.out_idx:, :]


class GenomeReaderWriter(GenomeReader, GenomeWriter):
    pass
