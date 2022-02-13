from core.game.util import get_player, run_game, get_result

def run_sims(s1, s2, args):
    import time
    from progress.bar import IncrementalBar

    n_games = args.ngames
    depths  = range(args.max_depth + 1)

    result_list = []

    # Start the loop over n_games simulations
    message = f'Running {n_games} iterations of Mancala with player one and two strategies: "{s1}" and "{s2}", respectively.'
    print(message)
    for depth in depths:
        print(f'Switching to depth {depth}')
        with IncrementalBar('Progress: ', max=n_games) as bar:
            for game in range(n_games):

                start_time = time.time()

                player_one = get_player(s1, 1)
                player_two = get_player(s2, 2)

                # use game iteration as seed for reproducability, ensuring seed is never 0
                if hasattr(player_one, 'set_seed'):
                    seed_one = 2 * n_games + game
                    player_one.set_seed(seed_one)

                if hasattr(player_two, 'set_seed'):
                    seed_two = 2 * n_games - game
                    player_two.set_seed(seed_two)

                if s1 == 'min_max':
                    player_one.depth = depth
                    if args.no_alpha_beta_pruning:
                        player_one.pruning = False

                if s2 == 'min_max':
                    player_two.depth = depth
                    if args.no_alpha_beta_pruning:
                        player_two.pruning = False

                # run this game according to the defined rules and the player strategies for move choice
                data = run_game(player_one, player_two, game+1, args)
                end_time = time.time()
                data['game_run_time'] = end_time - start_time
                data['depth']         = depth
                result_list.append(data)

                bar.next()

    return get_result().append(result_list)

# ====================================================================================================

def main(args):

    if args.n_marbles is not None and args.n_marbles > 0:
        print(f'Setting initial number of marbles to {args.n_marbles}')

    #result = run_sims('min_max', 'min_max', args)
    result = run_sims('min_max', 'max_score', args)

    output = f'data/{args.output}.csv'
    print(f'Saving output to {output}')
    result.to_csv(output, index=False)

# ====================================================================================================

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--ngames',
            default = 100,
            type = int,
            help = 'Number of independent mancala games to run')

    parser.add_argument('-o', '--output',
            required = True,
            help = 'output file')

    parser.add_argument('--max-depth',
            default = 7,
            type = int,
            help = 'Maximum depth to consider for min_max')

    parser.add_argument('--n-marbles',
            default = 4,
            required = False,
            type = int,
            help = 'Number of initial marbles in buckets')

    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'Verbose output')

    parser.add_argument('--no-alpha-beta-pruning',
            default = False,
            action = 'store_true',
            help = 'Switch off alpha-beta pruning for the min_max strategy')

    args = parser.parse_args()

    main(args)
