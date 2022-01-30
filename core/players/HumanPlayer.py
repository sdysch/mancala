from core.players.Player import Player
from core.game.Board import Board

class HumanPlayer(Player):
    """Class that allows user input - a human player"""

    strategy = 'human'

    def __init__(self, player):

        self.player = player


    def move(self, board):
        """Choose a random move from board for player"""
        moves = board.available_moves(self.player)

        print(board)
        print(f'Please choose a move for player {self.player} from the available moves: {moves}')
        while True:
            try:
                move = int(input('Enter move: '))
            except ValueError:
                print(f'Invalid move choice, please choose from {moves}')
                continue

            if move in moves:
                break

            #print(board)
            print(f'Invalid move choice, please choose from {moves}')
        return move
