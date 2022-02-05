import unittest
from core.players.MaxMarblesPlayer import MaxMarblesPlayer
from core.game.Board import Board

class TestMaxMarblesPlayer(unittest.TestCase):

    def test_moves(self):
        player = MaxMarblesPlayer(1)
        board = Board()
        board.player_one_cups = [6, 5, 4, 3, 2, 1]

        move = player.move(board)
        self.assertEqual(move, 1)

    def test_moves_1(self):
        player = MaxMarblesPlayer(1)
        board = Board()
        board.player_one_cups = [0, 0, 3, 10, 34]

        move = player.move(board)
        self.assertEqual(move, 5)

if __name__ == '__main__':
    unittest.main()
