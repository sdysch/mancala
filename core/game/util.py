# Helper functions for game simulations

# ====================================================================================================

def run_trials(args):
    """Iterate through a full mancala game, args.ngames times"""

    import pandas as pd 
    import time

    from progress.bar import IncrementalBar

    n_games = args.ngames

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
        'first_move',
        'player_one_strategy',
        'player_two_strategy',
    ]

    result = pd.DataFrame(columns=columns)

    start_time = time.time()

    if args.make_runtime_plots:
        runtime = []

    # Start the loop over n_games simulations
    # TODO multithreading? This is essentially O(n), so it probably won't do much. Maybe multi-processing?
    message = f'Running {n_games} iterations of Mancala with player one and two strategies: "{args.player_one_strategy}" and "{args.player_two_strategy}", respectively.'
    print(message)
    with IncrementalBar('Progress: ', max=n_games) as bar:
        for game in range(n_games):

            player_one = get_player(args.player_one_strategy, 1)
            player_two = get_player(args.player_one_strategy, 2)

            # use game iteration as seed for reproducability, ensuring seed is never 0
            seed_one = 2 * n_games + game
            seed_two = 2 * n_games - game

            player_one.set_seed(seed_one)
            player_two.set_seed(seed_one)

            # run this game according to the defined rules and the player strategies for move choice
            df = run_game(player_one, player_two)
            result = result.append(df, ignore_index=True)

            if args.make_runtime_plots:
                runtime.append(time.time() - start_time)
            bar.next()

    print(f'Ran {n_games} iterations in {time.time() - start_time} seconds')

    # runtime plots
    if args.make_runtime_plots:
        from core.plotting.util import make_runtime_plot
        make_runtime_plot(runtime, args.output)

    if args.make_runtime_plots and args.save_runtime_list:
        # pickle list
        import pickle
        pickle.dump(runtime, open(f'plots/{args.output}.p', 'wb'))

    return result

# ====================================================================================================

def run_game(player_one, player_two):
    """ Run a single mancala game"""

    from core.game.Board import Board
    board = Board()

    board.run_full_game(player_one, player_two)
    board.calculate_final_board_scores()

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

def get_player(strategy, player_number):

    if strategy == 'random':
        from core.players.RandomPlayer import RandomPlayer
        return RandomPlayer(player_number)
    else:
        raise ValueError(f'Strategy {strategy} is not recognised')

# ====================================================================================================
