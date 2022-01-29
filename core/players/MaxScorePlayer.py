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

    def move(self, board):
        """Choose the move from board to maximise the player's score.
            If there are multiple possible moves, then the choice is random"""

        from copy import deepcopy

        if board.player != self.player:
            raise ValueError(f'board player is {board.player} and MaxScorePlayer is {self.player}. Please check your logic')

        print(f'Board: \n{board}')
        moves = board.available_moves(self.player)

        player = 1 if self.player == 1 else 2
        initial_score = board.get_player_goal(player)
        score_move_holder = {}

        # Examine all moves. A player ending in their goal is counted as the end of their move
        print(f'Available moves for player {self.player}: {moves}')
        for move in moves:
            board_copy = deepcopy(board)
            print(f'Trying move {move} for player {board_copy.player} on side {board_copy.side}')
            print(board_copy)
            bucket     = move
            player     = board_copy.player
            side       = board_copy.side
            position   = board_copy.position
            first_move = True
            while True:
                print(board_copy)
                print(side, position)
                # ended in player goal
                if side == None and position == 0:
                    if not first_move:
                        print('Ended in player goal')
                        print(board_copy)
                        break
                    side = player
                    board_copy.make_player_move(player, bucket, side)

                # last marble was put into an empty bucket
                elif not first_move and board_copy.last_bucket_empty(side, position):
                    print('Last marble went into empty bucket')
                    print(board_copy)
                    break

                # same player continues from the position the previous move terminated in
                else:
                    print(f'Now the player is {player}')
                    board_copy.make_player_move(player, bucket, side)
                    bucket = board_copy.position
                    side   = board_copy.side
                    first_move = False
            score_move_holder[move] = board_copy.get_player_goal(player) - initial_score

        print(score_move_holder)
        max_score = max(score_move_holder.values())
        print(max_score)

        # find max score, and corresponding move
        choices = []
        for move, score in score_move_holder.items():
            if score == max_score:
                choices.append(move)

        if len(choices) == 1:
            choice = choices[0]
        else:
            choice = self.rng.choice(choices)

        print(choice)
        return choice
