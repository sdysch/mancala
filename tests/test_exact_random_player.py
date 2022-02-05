import unittest
from core.players.ExactRandomPlayer import ExactRandomPlayer
from core.game.Board import Board

class TestExactRandomPlayer(unittest.TestCase):

    def test_moves(self):
        player = ExactRandomPlayer(1)
        board = Board()
        board.player_one_cups = [6, 5, 4, 3, 2, 1]

        move = player.move(board)
        self.assertEqual(move, 6)

    def test_moves_1(self):
        player = ExactRandomPlayer(1)
        board = Board()
        board.player_one_cups = [0, 0, 6, 0, 0, 0]

        move = player.move(board)
        self.assertEqual(move, 3)

    def test_moves_2(self):
        player = ExactRandomPlayer(1)
        board = Board()
        board.player_one_cups = [0, 0, 0, 0, 2, 0]

        move = player.move(board)
        self.assertEqual(move, 5)

if __name__ == '__main__':
    unittest.main()
