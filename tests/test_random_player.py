import unittest
from core.players.RandomPlayer import RandomPlayer
from core.game.Board import Board

class TestRandomPlayer(unittest.TestCase):

    def test_random_player_seed(self):
        player = RandomPlayer(1)
        self.assertEqual(player.seed, 0)

    def test_random_player_seed_1(self):
        player = RandomPlayer(1)
        board = Board()
        board.player_one_cups = [1, 2, 3, 0, 4, 5]

        move = player.move(board)
        self.assertTrue(move in [1, 2, 3, 5, 6])

if __name__ == '__main__':
    unittest.main()
