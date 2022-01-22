# helper functions for players

def get_player(strategy, player_number):

    if strategy == 'random':
        from core.players.RandomPlayer import RandomPlayer
        return RandomPlayer(player_number)
    else:
        raise ValueError(f'Strategy {strategy} is not recognised')

# ====================================================================================================
