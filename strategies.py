# global variables
STRATEGIES = [
        'random'
        ]
INITIAL_PLAYER = 1

# ====================================================================================================

def main(args):

    global STRATEGIES

    if args.player_one_strategy not in STRATEGIES or args.player_two_strategy not in STRATEGIES:
        raise ValueError(f'One strategy is not recognised. Please choose from {STRATEGIES}')
    else:
        result = run_trials(args)
        output = f'data/{args.output}.csv'
        print(f'Saving output to {output}')
        result.to_csv(output, index=False)

# ====================================================================================================

def run_trials(args):
    """Iterate through a full mancala game, args.ngames times"""

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

    import time
    start_time = time.time()

    if args.make_runtime_plots:
        runtime = []

    # TODO multithreading? This is essentially O(n), so it probably won't do much
    # Maybe multi-processing?
    from progress.bar import IncrementalBar
    message = f'Running {n_games} iterations of Mancala with player one and two strategies: "{args.player_one_strategy}" and "{args.player_two_strategy}", respectively.'
    with IncrementalBar(message, max=n_games) as bar:
        for game in range(n_games):

            player_one = get_player(args.player_one_strategy, 1)
            player_two = get_player(args.player_one_strategy, 2)

            if player_one is None:
                raise ValueError('Player one is None')

            if player_two is None:
                raise ValueError('Player two is None')

            # use game iteration as seed for reproducability, ensuring seed is never 0
            seed_one = 2 * n_games + game
            seed_two = 2 * n_games - game

            player_one.set_seed(seed_one)
            player_two.set_seed(seed_one)

            df = run_game(player_one, player_two)
            result = result.append(df, ignore_index=True)

            if args.make_runtime_plots:
                runtime.append(time.time() - start_time)
            bar.next()

    print(f'Ran {n_games} iterations in {time.time() - start_time} seconds')

    # runtime plots
    if args.make_runtime_plots:
        import matplotlib.pyplot as plt
        plt.plot(runtime)
        plt.xlabel('Number of games')
        plt.ylabel('Time [seconds]')
        plt.savefig(f'plots/runtime_{args.output}.pdf')
        plt.savefig(f'plots/runtime_{args.output}.png')

        # pickle list
        import pickle
        pickle.dump(runtime, open(f'plots/{args.output}.p', 'wb'))

    return result

# ====================================================================================================

def get_player(strategy, player_number):

    global STRATEGIES

    if strategy not in STRATEGIES:
        raise ValueError(f'Strategy {strategy} is not recognised')

    if strategy == 'random':
        from core.players.RandomPlayer import RandomPlayer
        return RandomPlayer(player_number)
    else:
        return None

# ====================================================================================================

def run_game(player_one, player_two):
    """ Run a single mancala game"""

    from core.game.Board import Board
    board = Board()

    board = make_moves(board, player_one, player_two)

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
        'player_1_score'      : board.player_one_goal,
        'player_2_score'      : board.player_two_goal,
        'player_1_moves'      : board.n_moves_player_one,
        'player_2_moves'      : board.n_moves_player_two,
        'total_moves'         : board.n_moves,
        'n_start_marbles'     : board._N_MARBLES,
        'n_cups'              : board._NCUPS,
        'player_1_result'     : player_1_result,
        'player_2_result'     : player_2_result,
        'first_move'          : board.first_move if hasattr(board, 'first_move') else None,
        'player_one_strategy' : player_one.strategy,
        'player_two_strategy' : player_two.strategy
    }
    return results

# ====================================================================================================

def make_moves(board, player_one, player_two):
    """ make moves with """

    global INITIAL_PLAYER

    player         = INITIAL_PLAYER
    initial_side   = player
    if INITIAL_PLAYER == 1:
        initial_choice = player_one.move(board)
    else:
        initial_choice = player_two.move(board)

    # can't think of a better way to store this
    setattr(board, 'first_move', initial_choice)

    # make initial move
    side, position = board.make_player_move(player, initial_choice, initial_side)

    while not board.no_more_moves():

        # ended in player goal - they get a new move
        if side == None and position == 0:
            move = player_one.move(board) if player == 1 else player_two.move(board)
            side, position = board.make_player_move(player, move, player)

        # if the last marble was put into an empty bucket, the players switch
        elif board.last_bucket_empty(side, position):
            player = 1 if player == 2 else 2
            side_of_board = player
            move = player_one.move(board) if player == 1 else player_two.move(board)
            side, position = board.make_player_move(player, move, side_of_board)

        # same player continues from the position the previous move terminated in
        else:
            side, position = board.make_player_move(player, position, side)

    #print(board)
    board.calculate_final_board_scores()

    return board

# ====================================================================================================

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--ngames',
            default = 10000,
            type = int,
            help = 'Number of independent mancala games to run')

    parser.add_argument('--player-one-strategy',
            default = 'random', 
            type = str,
            help = 'Strategy for player one. Default: random')

    parser.add_argument('--player-two-strategy',
            default = 'random', 
            type = str,
            help = 'Strategy for player two. Default: random')

    parser.add_argument('-o', '--output',
            default = 'output', 
            type = str,
            help = 'Stamp for outputs')

    parser.add_argument('--make-runtime-plots',
            default = True,
            type = bool,
            help = 'Plot runtime vs number of games simulated')

    args = parser.parse_args()

    main(args)
