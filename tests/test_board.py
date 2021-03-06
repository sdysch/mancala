import unittest
from core.game.Board import Board

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.b = Board()

    def tearDown(self):
        del self.b

    def test_player_one_moves(self):
        self.b.player_one_cups = [0, 0, 0, 0, 0, 6]
        self.b.player_two_cups = [0, 0, 0, 0, 0, 0]

        self.b.make_player_move(1, 6, 1)

        result = Board()
        result.player_one_goal = 1
        result.player_one_cups = [0, 0, 0, 0, 0, 0]
        result.player_two_cups = [1, 1, 1, 1, 1, 0]

        self.assertEqual(self.b.player_one_cups, result.player_one_cups) \
        and self.assertEqual(self.b.player_two_cups, result.player_two_cups) \
        and self.assertEqual(self.b.player_one_goal, result.player_one_goal) \
        and self.assertEqual(self.b.player_two_goal, result.player_two_goal)

    def test_player_two_moves(self):
        self.b.player_one_cups = [1, 1, 1, 1, 1, 1]
        self.b.player_two_cups = [0, 0, 7, 0, 0, 0]

        self.b.make_player_move(2, 3, 2)

        result = Board()
        result.player_two_goal = 1
        result.player_one_cups = [2, 2, 2, 1, 1, 1]
        result.player_two_cups = [0, 0, 0, 1, 1, 1]

        self.assertEqual(self.b, result)

    def test_player_one_move_fail(self):
        self.b.player_one_cups = [0, 0, 7, 0, 0, 0]

        self.assertRaises(ValueError, self.b.make_player_move, 1, 0, 1)

    def test_player_two_move_fail(self):
        self.b.player_two_cups = [0, 0, 7, 0, 0, 0]

        self.assertRaises(ValueError, self.b.make_player_move, 2, 0, 2)

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
        self.b.make_player_move(1, 4, 1)

        self.assertEqual((self.b.side, self.b.position), (None, 0))

    def test_end_in_goal_2(self):
        self.b.player_two_cups = [0, 0, 0, 3, 0, 0]
        self.b.make_player_move(2, 4, 2)

        self.assertEqual((self.b.side, self.b.position), (None, 0))

    def test_available_moves_1(self):

        self.assertEqual(self.b.available_moves(1), [v + 1 for v in range(6)])

    def test_available_moves_2(self):
        self.b.player_one_cups = [0, 0, 0, 0, 0, 0]

        self.assertEqual(self.b.available_moves(1), [])

    def test_last_bucket_empty_1(self):

        self.b.position = 0
        self.assertRaises(ValueError, self.b.last_bucket_empty)

    def test_last_bucket_empty_2(self):

        self.b.player_one_cups = [0, 0, 0, 0, 3, 0]
        self.b.player_two_cups = [0, 0, 0, 0, 4, 0]
        self.b.make_player_move(1, 5, 1)

        self.assertEqual(self.b.last_bucket_empty(), True)

    def test_last_bucket_empty_3(self):

        self.b.player_one_cups = [0, 3, 0, 0, 0, 0]
        self.b.make_player_move(1, 2, 1)

        self.assertEqual(self.b.last_bucket_empty(), True)

    def test_last_bucket_empty_4(self):

        self.b.player_one_cups = [0, 0, 0, 0, 5, 0]
        self.b.player_two_cups = [0, 6, 0, 0, 0, 3]
        self.b.make_player_move(2, 6, 2)

        self.assertEqual(self.b.last_bucket_empty(), True)

    def test_last_bucket_empty_5(self):

        self.b.player_two_cups = [0, 3, 0, 0, 0, 3]
        self.b.make_player_move(2, 2, 2)

        self.assertEqual(self.b.last_bucket_empty(), True)

    def test_iterate(self):

        self.b.player_two_cups = [0, 2, 3, 0, 0, 3]
        self.b.player_one_cups = [4, 4, 4, 4, 4, 3]

        self.b.iterate_until_turn_over(1, 6)

        result = Board()
        result.player_one_cups = [4, 4, 4, 4, 4, 0]
        result.player_two_cups = [3, 1, 1, 4, 0, 1]

        self.assertEqual(self.b.player_one_cups, result.player_one_cups) \
        and self.assertEqual(self.b.player_two_cups, result.player_two_cups)

    def test_deep_copy(self):
        from copy import deepcopy

        self.b.player_one_cups = [1, 2, 3, 4, 5]
        copied = deepcopy(self.b)
        copied.player_one_cups = [5, 4, 3, 2, 1]

        self.assertNotEqual(copied.player_one_cups, self.b.player_one_cups)

if __name__ == '__main__':
    unittest.main()
