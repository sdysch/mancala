import unittest
from Board import Board

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.b = Board()

    def tearDown(self):
        del self.b

    def test_player_one_moves(self):
        self.b.player_one_cups = [0, 0, 0, 0, 0, 6]
        self.b.player_two_cups = [0, 0, 0, 0, 0, 0]

        self.b.make_player_move(1, 6)

        result = Board()
        result.player_one_goal = 1
        result.player_one_cups = [0, 0, 0, 0, 0, 0]
        result.player_two_cups = [1, 1, 1, 1, 1, 0]

        self.assertEqual(self.b, result)

    def test_player_two_moves(self):
        self.b.player_one_cups = [1, 1, 1, 1, 1, 1]
        self.b.player_two_cups = [0, 0, 7, 0, 0, 0]

        self.b.make_player_move(2, 3)

        result = Board()
        result.player_two_goal = 1
        result.player_one_cups = [2, 2, 2, 1, 1, 1]
        result.player_two_cups = [0, 0, 0, 1, 1, 1]

        self.assertEqual(self.b, result)

    def test_player_one_move_fail(self):
        self.b.player_one_cups = [0, 0, 7, 0, 0, 0]

        self.assertRaises(ValueError, self.b.make_player_move, 1, 0)

    def test_player_two_move_fail(self):
        self.b.player_two_cups = [0, 0, 7, 0, 0, 0]

        self.assertRaises(ValueError, self.b.make_player_move, 2, 0)

    def test_no_more_moves_1(self):
        self.b.player_one_cups = [1, 1, 1, 1, 1, 1]
        self.b.player_two_cups = [0, 0, 0, 0, 0, 0]

        self.assertEqual(self.b.no_more_moves(), True)

    def test_no_more_moves_2(self):
        self.b.player_one_cups = [0, 0, 0, 0, 0, 0]
        self.b.player_two_cups = [0, 0, 4, 0, 0, 0]

        self.assertEqual(self.b.no_more_moves(), True)

    def test_no_more_moves_2(self):
        self.b.player_one_cups = [0, 3, 0, 0, 0, 0]
        self.b.player_two_cups = [0, 0, 4, 0, 0, 0]

        self.assertEqual(self.b.no_more_moves(), False)

    def test_end_in_goal_1(self):
        self.b.player_one_cups = [0, 0, 0, 3, 0, 0]

        self.assertEqual(self.b.make_player_move(1, 4), True)

    def test_end_in_goal_2(self):
        self.b.player_two_cups = [0, 0, 0, 3, 0, 0]

        self.assertEqual(self.b.make_player_move(2, 4), True)

    def test_not_end_in_goal_1(self):
        self.b.player_one_cups = [0, 0, 0, 4, 0, 0]

        self.assertEqual(self.b.make_player_move(1, 4), False)

    def test_not_end_in_goal_2(self):
        self.b.player_two_cups = [0, 2, 0, 0, 0, 0]

        self.assertEqual(self.b.make_player_move(2, 2), False)

if __name__ == '__main__':
    unittest.main()
