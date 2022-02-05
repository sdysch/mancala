from abc import ABC, abstractmethod

class Player(ABC):
    """Abstract class to simulate Mancala player behaviour with a defined strategy"""

    @abstractmethod
    def move(self, board=None):
        """Return a move choice for board"""
        pass
