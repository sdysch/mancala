import unittest
from core.Player import Player

class TestPlayer(unittest.TestCase):

    def test_player_init(self):
        player = Player()
        self.assertRaises(NotImplementedError, player.move, None)

if __name__ == '__main__':
    unittest.main()
