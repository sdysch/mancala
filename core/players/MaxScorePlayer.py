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
            bucket = move
            player = board_copy.player
            side   = board_copy.side
            first_move = True
            while True:
                # ended in player goal
                if board_copy.side == None and board_copy.position == 0:
                    print('Ended in player goal')
                    print(board_copy)
                    break
                if not first_move:
                    # last marble put into an empty bucket
                    if board_copy.last_bucket_empty(board_copy.side, board_copy.position):
                        print('Last marble went into empty bucket')
                        print(board_copy)
                        break

                board_copy.make_player_move(board_copy.player, bucket, side)
                bucket = board_copy.position
                side   = board_copy.side
                first_move = False
                print(f'Bucket is now {bucket}')
                print(f'Player is now {player}')
                print(f'side is now {side}')

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
            return choices[0]
        
        return self.rng.choice(choices)
