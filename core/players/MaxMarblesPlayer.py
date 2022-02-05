from core.players.Player import Player
from core.game.Board import Board
from random import Random

class MaxMarblesPlayer(Player):
    """ Player strategy that makes the move corresponding to the bucket with the most marbles in it.
        If multiple such moves are possible, then a random choice is made.
    """

    strategy = 'max_marbles'

    def __init__(self, player, seed=0):

        self.seed = seed
        self.rng  = Random()
        self.rng.seed(self.seed)
        self.player = player


    def set_seed(self, seed):
        self.seed = seed
        self.rng.seed(seed)

    def move(self, board):
        cups = board.get_player_cups(self.player)
        moves = board.available_moves(self.player)
        max_marbles = max(cups)
        choices = [v for v in moves if cups[v - 1] == max_marbles]
        move = self.rng.choice(choices)

        return move
