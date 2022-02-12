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

    def get_move_with_max_score(self, score_move_holder):
        """ Find maximum score from dict[moves] = scores, return move corresponding to it """
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

        return self.get_move_with_max_score(score_move_holder)

    def get_move_score(self, move, board, first_move=True):

        # FIXME - Don't repeat yourself! Re-use Board.iterate_until_over!

        from copy import deepcopy
        board_copy = deepcopy(board)
        board_copy.position = move
        board_copy.side     = self.player

        while True:

            # check if there are possible moves to make
            if board_copy.no_more_moves():
                board_copy.calculate_final_board_scores()
                return self.score(board_copy)

            # examine mancala rules

            # if previous move ended in player goal, player gets a new choice
            # we recursively find the best move choice
            if board_copy.side == None and board_copy.position == 0:
                moves_scores = {}
                for move in board_copy.available_moves(self.player):
                    moves_scores[move] = self.get_move_score(move, board_copy)
                choice = self.get_move_with_max_score(moves_scores)
                return self.score(board_copy) + moves_scores[choice]

            # if previous move ended in empty bucket, players switch and we are done with this move tree.
            elif board_copy.last_bucket_empty():
                return self.score(board_copy)

            # if none of the previous rules apply, we must have ended on a non-empty bucket
            # carry on iterating
            else:
                board_copy.make_player_move(board_copy.player, board_copy.position, board_copy.side)
