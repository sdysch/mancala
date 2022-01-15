# global variables
STRATEGIES = [
        'random'
        ]
INITIAL_PLAYER = 1

# ====================================================================================================

def main(args):

    global STRATEGIES

    if args.strategy not in STRATEGIES:
        raise ValueError(f'Strategy {args.strategy} is not recognised')
    else:
        result = run_random_trials(args)

# ====================================================================================================

def run_random_trials(args):
    """ Iterate through a full mancala game, args.ngames times.
        The player's moves are selected with equal probability from the available legal moves. """

    n_games = args.ngames

    import pandas as pd 

    # data structure to store results
    columns = [
        'player_1_result',
        'player_2_result',
        'player_1_score',
        'player_2_score',
        'player_1_moves',
        'player_2_moves',
    ]

    result = pd.DataFrame(columns=columns)

    print(f'Running {n_games} iterations of Mancala with random strategy')
    import time
    start_time = time.time()

    # TODO multithreading?
    for game in range(n_games):
        # use game iteration as seed for reproducability
        seed = game + 1
        result.append(run_random_game(seed))

    print(f'Ran {n_games} iterations in {time.time() - start_time} seconds')

    return result

# ====================================================================================================

def run_random_game(seed):
    """ Run a single mancala game with random strategy """

    from Board import Board
    board = Board()

    board = make_moves(board, strategy='random', seed=seed)
    # print(f'Player 1 score: {board.player_one_goal}')
    # print(f'Player 2 score: {board.player_two_goal}')
    # print(f'Player 1 moves: {board.n_moves_player_one}')
    # print(f'Player 2 moves: {board.n_moves_player_two}')
    # print(f'Total moves: {board.n_moves}')

# ====================================================================================================

def make_moves(board, strategy, **kwargs):
    """ make moves with strategy. side, position, board represent the initial choices/board layout """

    global STRATEGIES, INITIAL_PLAYER

    if strategy not in STRATEGIES:
        raise ValueError(f'Strategy {args.strategy} is not recognised')

    if strategy == 'random':
        seed = kwargs.get('seed', 'DEFAULT')

        if seed == 'DEFAULT':
            raise ValueError('Strategy is random and no seed specified')

        from random import Random
        rng = Random()
        rng.seed(seed)

        player         = INITIAL_PLAYER
        initial_side   = player
        initial_choice = rng.choice(board.available_moves(player))

        # make initial move
        side, position = board.make_player_move(player, initial_choice, initial_side)


    while not board.no_more_moves():

        # ended in player goal - they get a new move
        if side == None and position == 0:
            moves = board.available_moves(player)
            move  = get_move(board, moves, strategy, rng)
            side, position = board.make_player_move(player, move, player)

        # if the last marble was put into an empty bucket, the players switch
        elif board.last_bucket_empty(side, position):
            player = 1 if player == 2 else 2
            side_of_board = player
            moves = board.available_moves(player)
            move  = get_move(board, moves, strategy, rng)
            side, position = board.make_player_move(player, move, side_of_board)

        # same player continues from the position the previous move terminated in
        else:
            side, position = board.make_player_move(player, position, side)

    #print(board)
    board.calculate_final_board_scores()

    return board

# ====================================================================================================

def get_move(board, moves, strategy, rng):
    """ Get move with strategy """

    global STRATEGIES

    if strategy not in STRATEGIES:
        raise ValueError(f'Strategy {args.strategy} is not recognised')

    move = None
    if strategy == 'random':
        move = rng.choice(moves)

    return move

# ====================================================================================================
            
if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--ngames',
            default = 10000,
            type = int,
            help = 'Number of independent mancala games to run')

    parser.add_argument('-s', '--strategy',
            default = 'random', 
            type = str,
            help = 'Strategy to choose moves. Default: random')

    args = parser.parse_args()

    main(args)
