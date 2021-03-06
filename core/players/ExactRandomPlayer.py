from core.players.RandomPlayer import RandomPlayer
from core.game.Board import Board
from random import Random

class ExactRandomPlayer(RandomPlayer):
    """ Player strategy that makes moves favouring not giving up the turn.
        If no possible moves are possible, then the player defaults to a random player choice.
        If multiple such moves are possible, then the closest to the player's goal is taken, allowing
        for multiple moves of this kind to be played.
    """

    strategy = 'exact_random'

    def __init__(self, player, seed=0):

        super().__init__(player, seed)

    def move(self, board):

        exact_moves = []
        cups = board.get_player_cups(self.player)
        ncups = len(cups)

        for i, marbles in enumerate(cups):
            if marbles == 0:
                continue
            if ncups - i == marbles:
                exact_moves.append(i + 1)

        if len(exact_moves) == 0:
            return super().move(board)
        else:
            return exact_moves[-1]
