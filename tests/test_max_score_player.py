import unittest
from core.players.MaxScorePlayer import MaxScorePlayer
from core.game.Board import Board

class TestMaxScorePlayer(unittest.TestCase):

    def test_max_score_player_1(self):
        player = MaxScorePlayer(1)
        board = Board()
        board.player_one_cups = [1, 2, 3, 0, 0, 0]

        self.assertEqual(player.move(board), 2)

    def test_max_score_player_2(self):
        player = MaxScorePlayer(1)
        board = Board()
        board.player_two_cups = [1, 1, 1, 1, 1, 1]
        board.player_one_cups = [0, 0, 0, 0, 2, 1]

        self.assertEqual(player.move(board), 5)

    def test_max_score_player_3(self):
        player = MaxScorePlayer(1)
        board = Board()
        board.player_two_cups = [1, 1, 1, 1, 1, 1]
        board.player_one_cups = [0, 1, 0, 4, 0, 0]
        print(player.move(board))

        self.assertEqual(player.move(board), 4)

if __name__ == '__main__':
    unittest.main()
