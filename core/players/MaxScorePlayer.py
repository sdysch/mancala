from core.players.Player import Player
from core.game.Board import Board
from random import Random

class MaxScorePlayer(Player):
    """Class that simulates a player making the move which maximises the score"""

    strategy = 'max_score'

    def __init__(self, player, seed=0):

        self.seed = seed
        self.rng  = Random()
        self.rng.seed(self.seed)
        self.player = player

    def set_seed(self, seed):
        self.seed = seed
        self.rng.seed(seed)

    def score(self, board):
        return board.get_player_goal(self.player)

    def move(self, board):
        """Choose the move from board to maximise the player's score.
            If there are multiple possible moves, then the choice is random"""

        if board.player != self.player:
            raise ValueError(f'board player is {board.player} and MaxScorePlayer is {self.player}. Please check your logic')

        moves = board.available_moves(self.player)

        initial_score = board.get_player_goal(self.player)
        score_move_holder = {}

        # Examine all moves
        for move in moves:
            score = self.get_move_score(move, board)
            score_move_holder[move] = score

        max_score = max(score_move_holder.values())

        # find max score, and corresponding move
        choices = []
        for move, score in score_move_holder.items():
            if score == max_score:
                choices.append(move)

        if len(choices) == 1:
            choice = choices[0]
        else:
            choice = self.rng.choice(choices)

        return choice

    def get_move_score(self, move, board):
        from copy import deepcopy
        board_copy = deepcopy(board)
        board_copy.position = move
        board_copy.side     = self.player
        first_move = True

        while True:
            # ended in player goal
            if board_copy.side == None and board_copy.position == 0:
                break
            if not first_move:
                # ended in empty bucket, players switch
                if board_copy.last_bucket_empty(board_copy.side, board_copy.position):
                    break
            board_copy.make_player_move(board_copy.player, board_copy.position, board_copy.side)
            first_move = False
        return self.score(board_copy)
