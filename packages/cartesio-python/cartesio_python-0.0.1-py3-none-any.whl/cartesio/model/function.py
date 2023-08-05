from abc import ABC, abstractmethod
from typing import List


class GraphNode(ABC):
    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity


class FunctionNode(GraphNode, ABC):
    def __init__(self, name: str, arity: int, n_parameters: int):
        super().__init__(name, arity)
        self.n_parameters = n_parameters

    @abstractmethod
    def __call__(self, inputs: List, p: List):
        pass


class FunctionNodeWritable(FunctionNode, ABC):
    @abstractmethod
    def to_python(self, input_names: List, p: List, output_name: str):
        pass

    @abstractmethod
    def to_cpp(self, input_names: List, p: List, output_name: str):
        pass
