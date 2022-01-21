class Player:
    """Abstract class to simulate Mancala player behaviour with a defined strategy"""

    def move(self, board=None):
        """Return a move choice for board"""
        raise NotImplementedError(f'The player class is not inteded to be directly initiated. Please choose a derived class instead')
