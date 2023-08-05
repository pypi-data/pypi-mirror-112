from abc import abstractmethod, ABC  # Abstract Base Classes
from typing import List


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject, message_type):
        """
        Receive update from subject.
        """
        pass


class Observable(ABC):
    """
    The Observable owns some important state and notifies observers
    when the state changes.
    """

    _state: int = None
    """
    For the sake of simplicity, the Observable's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers: List[Observer] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer: Observer) -> None:
        print("Observable: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def clear(self) -> None:
        self._observers = []

    """
    The subscription management methods.
    """

    def notify(self, state) -> None:
        """
        Trigger an update in each subscriber.
        """

        self._state = state
        for observer in self._observers:
            observer.update(self)
