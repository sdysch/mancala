# TODO alpha-beta pruning to speedup
from core.players.Player import Player
from core.game.Board import Board
from copy import deepcopy
from random import Random

class MinMaxPlayer(Player):
    """Class that implements minmax strategy"""

    strategy = 'min_max'

    def __init__(self, player, seed=0, depth=3):

        self.player = player
        self.depth = depth
        self.seed = seed
        self.rng  = Random()
        self.rng.seed(self.seed)

    def set_seed(self, seed):
        self.seed = seed
        self.rng.seed(seed)

    def score(self, board):
        score_difference = board.player_one_goal - board.player_two_goal
        if self.player == 2:
            score_difference *= -1
        return score_difference

    def get_move_from_choice(self, score_move_holder, maximising):
        """ Find maximum (minimum) score from dict[moves] = scores if maximising=True (False), return move corresponding to it """
        score = max(score_move_holder.values()) if maximising else min(score_move_holder.values())

        # find max score, and corresponding move
        choices = []
        for move, _score in score_move_holder.items():
            if _score == score:
                choices.append(move)

        if len(choices) == 1:
            choice = choices[0]
        else:
            choice = self.rng.choice(choices)
    
        return choice

    def move(self, board):
        moves = board.available_moves(self.player)

        scores = { move : self.min_max(move, board, self.depth, True) for move in moves }

        return self.get_move_from_choice(scores, True)

    def min_max(self, move, b, depth, maximising):
        board = deepcopy(b)

        if depth == 0 or board.no_more_moves():
            if board.no_more_moves():
                board.calculate_final_board_scores()
            return self.score(board)

        board.position = move
        if board.side == None:
            board.side = board.player

        while True:

            # check if there are possible moves to make
            if board.no_more_moves():
                board.calculate_final_board_scores()
                return self.score(board)

            # recursively find the best move choice
            # ended in player's goal, they get a new move
            if board.side == None and board.position == 0:
                moves_scores = {}
                for move in board.available_moves(board.player):
                    moves_scores[move] = self.min_max(move, board, depth-1, maximising)
                choice = self.get_move_from_choice(moves_scores, maximising)
                return self.score(board) + moves_scores[choice]

            # if previous move ended in empty bucket, players switch and we are done with this move tree.
            elif board.last_bucket_empty():
                board.player = 1 if board.player == 2 else 2
                board.side = board.player
                moves_scores = {}
                for _move in board.available_moves(board.player):
                    moves_scores[_move] = self.min_max(_move, board, depth-1, not maximising)
                choice = self.get_move_from_choice(moves_scores, not maximising)
                return self.score(board) + moves_scores[choice]


            # if none of the previous rules apply, we must have ended on a non-empty bucket
            # carry on iterating
            else:
                board.make_player_move(board.player, board.position, board.side)
