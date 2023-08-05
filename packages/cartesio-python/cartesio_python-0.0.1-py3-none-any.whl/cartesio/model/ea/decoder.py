import numpy as np
import time

from cartesio.model.ea.genome import Genome, GenomeMetadata, GenomeReader
from cartesio.cv.function_set import FunctionSet

from typing import List

'''
class GenomeDecoder():
    @classmethod
    def from_json(cls, json_data):
        metadata = GenomeMetadata.from_json(json_data['metadata'])
        function_set = FunctionSet.from_json(json_data['functions'])
        if json_data['_endpoint']:
            endpoint = Endpoint.from_json(json_data['_endpoint'])
            return EndpointedCartesianGenomeDecoder(metadata, function_set, endpoint)
        return CartesianGenomeDecoder(metadata, function_set)
'''


class Decoder(GenomeReader):
    def __init__(self, metadata: GenomeMetadata, function_set: FunctionSet):
        super().__init__(metadata)
        self.function_set = function_set

    def to_json(self):
        decoding = {
            "metadata": {
                "rows": 1,  # single row CGP
                "columns": self._m.n_genes,
                "n_in": self._m.n_inputs,
                "n_out": self._m.n_outputs,
                "n_para": self._m.n_parameters,
                "n_conn": self._m.n_connections
            },
            "functions": self.function_set.ordered_list,
            "_endpoint": None
        }
        return decoding

    def __genome_to_one_graph(self, genome, root):
        next_indices = root.copy()
        output_tree = root.copy()
        while next_indices:
            next_index = next_indices.pop()
            if next_index < self._m.n_inputs:
                continue
            function_index = self.read_function(genome, next_index-self._m.n_inputs)
            active_connections = self.function_set.get_arity(function_index)
            next_connections = set(self.read_active_connections(genome, next_index-self._m.n_inputs, active_connections))
            next_indices = next_indices.union(next_connections)
            output_tree = output_tree.union(next_connections)
        return output_tree

    def read_active_nodes(self, G):
        # first, equivalent to update active nodes
        graphs = []
        outputs = self.read_outputs(G)

        for output in outputs:
            root = {output[self._m.con_idx]}
            one_graph = self.__genome_to_one_graph(G, root)
            graphs.append(sorted(list(one_graph)))

        return graphs

    def __decode_one(self, G: Genome, graphs: List, x: List):
        # fill output_map with inputs
        output_map = {i: x[i].copy() for i in range(self._m.n_inputs)}
        # now, execute the functions
        for graph in graphs:
            for node in graph:
                # inputs are already in the map
                if node < self._m.n_inputs:
                    continue
                node_index = node - self._m.n_inputs
                # fill the map with active nodes
                function_index = self.read_function(G, node_index)
                arity = self.function_set.get_arity(function_index)
                connections = self.read_active_connections(G, node_index, arity)
                inputs = [output_map[c] for c in connections]
                p = self.read_parameters(G, node_index)
                value = self.function_set.execute(function_index, inputs, p)

                output_map[node] = value

        return [output_map[output_gene[self._m.con_idx]] for output_gene in self.read_outputs(G)]

    def decode(self, G: Genome, x: List):
        """Decode the Genome given a list of inputs

        Args:
            G (Genome): [description]
            x (List): [description]

        Returns:
            [type]: [description]
        """
        all_y_pred = []
        all_times = []
        graphs = self.read_active_nodes(G)
        for xi in x:
            start_time = time.time()
            y_pred = self.__decode_one(G, graphs, xi)
            all_times.append(time.time() - start_time)
            all_y_pred.append(y_pred)
        whole_time = np.mean(np.array(all_times))
        return all_y_pred, whole_time


class EndpointedDecoder(Decoder):
    def __init__(self, metadata, function_set, endpoint):
        super().__init__(metadata, function_set)
        self.endpoint = endpoint

    def decode(self, G: Genome, x: List):
        all_y_pred, tmp_time = super().decode(G, x)
        new_all_y_pred = []
        supp_times = []
        for y_pred in all_y_pred:
            start_time = time.time()
            output = self.endpoint.execute(y_pred)
            supp_times.append(time.time() - start_time)
            new_all_y_pred.append(output)
        whole_time = np.mean(np.array(supp_times)) + tmp_time
        return new_all_y_pred, whole_time

    def to_json(self):
        decoding = super().to_json()
        decoding['_endpoint'] = self.endpoint.name
        return decoding
