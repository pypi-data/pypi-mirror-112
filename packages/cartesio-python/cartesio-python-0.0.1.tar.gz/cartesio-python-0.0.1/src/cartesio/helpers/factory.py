from abc import abstractmethod, ABC  # Abstract Base Classes


class Prototype(ABC):
    '''
    Using Prototype Pattern to duplicate:
    https://refactoring.guru/design-patterns/prototype
    '''
    @abstractmethod
    def clone(self):
        pass


class Factory(object):
    """
    Using Factory Pattern:
    https://refactoring.guru/design-patterns/factory-method
    """
    def __init__(self, prototype):
        self.set_prototype(prototype)

    def set_prototype(self, prototype):
        self._prototype = prototype

    def create(self):
        return self._prototype.clone()
