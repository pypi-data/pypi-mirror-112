import random
from abc import ABC, abstractmethod

from cartesio.cv.catalog import FunctionCatalog


class FunctionSet(ABC):
    def __init__(self):
        self.__functions = {}
        self.fill()

    def add_function(self, function_name):
        new_function_index = len(self.__functions)
        self.__functions[new_function_index] = FunctionCatalog.get(function_name)

    def add_function_set(self, function_set):
        for f in function_set.get_functions():
            self.add_function(f.name)

    def get_max_function_index(self):
        return len(self.__functions) - 1

    def get_functions(self):
        return list(self.__functions.values())

    def get_function_indices(self):
        return list(self.__functions.keys())

    def get_random_function_id(self):
        return random.choice(self.get_function_indices())

    def get_random_parameters_for_function(self, function_index):
        return self.__functions[function_index].get_random_parameters()

    def get_random_parameter_for_function(self, function_index, parameter_index):
        return self.__functions[function_index].get_random_parameters()

    def get_function_name(self, function_index):
        return self.__functions[function_index].name

    def execute(self, function_index, connections, parameters):
        return self.__functions[function_index](connections, parameters)

    def show(self):
        for index, function in self.__functions.items():
            print(f'[{index}] - {function.name}')

    def get_arity(self, function_index):
        return self.__functions[function_index].arity

    def get_n_parameters(self, function_index):
        return self.__functions[function_index].n_parameters

    @abstractmethod
    def fill(self):
        pass

    @property
    def max_arity(self):
        return max([self.get_arity(i) for i in self.get_function_indices()])

    @property
    def max_parameters(self):
        return max([self.get_n_parameters(i) for i in self.get_function_indices()])

    @property
    def n_functions(self):
        return len(self.__functions)

    @property
    def ordered_list(self):
        return [self.__functions[i].name for i in range(self.n_functions)]

    @classmethod
    def from_json(cls, json_data):
        function_set = EmptyFunctionSet()
        for f_name in json_data:
            function_set.add_function(f_name)
        return function_set


class EmptyFunctionSet(FunctionSet):
    def fill(self):
        pass
