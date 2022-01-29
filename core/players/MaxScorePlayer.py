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

    def move_score(self, board):
        return board.get_player_goal(self.player)

    def move(self, board):
        """Choose the move from board to maximise the player's score.
            If there are multiple possible moves, then the choice is random"""

        from copy import deepcopy

        if board.player != self.player:
            raise ValueError(f'board player is {board.player} and MaxScorePlayer is {self.player}. Please check your logic')

        #print(f'Board: \n{board}')
        moves = board.available_moves(self.player)

        initial_score = board.get_player_goal(self.player)
        score_move_holder = {}

        # Examine all moves
        #print(f'Available moves for player {self.player}: {moves}')
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.position = move
            board_copy.side     = self.player
            first_move = True
            #print(f'Trying move {move} for player {board_copy.player} on side {board_copy.side}')
            while True:
                #print(board_copy)
                if not first_move:
                    # ended in player goal
                    if board_copy.side == None and board_copy.position == 0:
                        #print('Ended in player goal')
                        #print(board_copy)
                        break
                    # ended in empty bucket, players switch
                    elif board_copy.last_bucket_empty(board_copy.side, board_copy.position):
                        #print('Ended in empty bucket')
                        #print(board_copy)
                        break
                board_copy.make_player_move(board_copy.player, board_copy.position, board_copy.side)
                first_move = False
            score_move_holder[move] = self.move_score(board_copy) - initial_score

        max_score = max(score_move_holder.values())
        #print(score_move_holder)
        #print(max_score)

        # find max score, and corresponding move
        choices = []
        for move, score in score_move_holder.items():
            if score == max_score:
                choices.append(move)

        if len(choices) == 1:
            choice = choices[0]
        else:
            choice = self.rng.choice(choices)

        #print(f'Move choice: {choice}')
        return choice
