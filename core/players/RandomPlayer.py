from core.players.Player import Player
from core.game.Board import Board
from random import Random

class RandomPlayer(Player):
    """Class that simulates a player making random choices from available mancala moves"""

    strategy = 'random'

    def __init__(self, player, seed=0):

        self.seed = seed
        self.rng  = Random()
        self.rng.seed(self.seed)
        self.player = player


    def set_seed(self, seed):
        self.seed = seed
        self.rng.seed(seed)

    def move(self, board):
        """Choose a random move from board for player"""
        moves = board.available_moves(self.player)
        move = self.rng.choice(moves)

        return move
