import unittest
from core.players.Player import Player

class TestPlayer(unittest.TestCase):

    def test_player_init(self):
        self.assertRaises(TypeError, Player)

if __name__ == '__main__':
    unittest.main()
