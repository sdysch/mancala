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
        print(f'Saving output to {args.output}')
        result.to_csv(args.output, index=False)

# ====================================================================================================

def run_random_trials(args):
    """ Iterate through a full mancala game, args.ngames times.
        The player's moves are selected with equal probability from the available legal moves. """

    n_games = args.ngames

    import pandas as pd 

    # data structure to store results
    columns = [
        'player_1_score',
        'player_2_score',
        'player_1_moves',
        'player_2_moves',
        'total_moves',
        'n_start_marbles',
        'n_cups',
        'player_1_result',
        'player_2_result',
        'first_move'
    ]

    result = pd.DataFrame(columns=columns)

    print(f'Running {n_games} iterations of Mancala with random strategy')
    import time
    start_time = time.time()

    # TODO multithreading? This is essentially O(n), so it probably won't do much
    # Maybe multi-processing?
    for game in range(n_games):
        # use game iteration as seed for reproducability
        seed = game + 1
        df = run_random_game(seed)
        result = result.append(df, ignore_index=True)

    print(f'Ran {n_games} iterations in {time.time() - start_time} seconds')

    return result

# ====================================================================================================

def run_random_game(seed):
    """ Run a single mancala game with random strategy """

    from core.game.Board import Board
    board = Board()

    board = make_moves(board, strategy='random', seed=seed)

    if board.player_one_goal > board.player_two_goal:
        player_1_result = 'win'
        player_2_result = 'lose'
    elif board.player_two_goal > board.player_one_goal:
        player_1_result = 'lose'
        player_2_result = 'win'
    elif board.player_two_goal == board.player_one_goal:
        player_1_result = 'draw'
        player_2_result = 'draw'

    results = {
        'player_1_score'  : board.player_one_goal,
        'player_2_score'  : board.player_two_goal,
        'player_1_moves'  : board.n_moves_player_one,
        'player_2_moves'  : board.n_moves_player_two,
        'total_moves'     : board.n_moves,
        'n_start_marbles' : board._N_MARBLES,
        'n_cups'          : board._NCUPS,
        'player_1_result' : player_1_result,
        'player_2_result' : player_2_result,
        'first_move'      : board.first_move if hasattr(board, 'first_move') else None
    }
    return results

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
        # can't think of a better way to store this
        setattr(board, 'first_move', initial_choice)

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

    parser.add_argument('-o', '--output',
            default = 'data/output.csv', 
            type = str,
            help = 'Location to save output file to')

    args = parser.parse_args()

    main(args)
