from core.game.util import get_player, run_game, get_result

def run_sims(s1, s2, args):
    import time
    from progress.bar import IncrementalBar

    n_games = args.ngames
    marbles  = range(1, args.max_n_marbles + 1)

    result_list = []

    # Start the loop over n_games simulations
    message = f'Running {n_games} iterations of Mancala with player one and two strategies: "{s1}" and "{s2}", respectively.'
    print(message)
    for init_marbles in marbles:
        print(f'Switching init number of marbles to {init_marbles}')
        args.n_marbles = init_marbles
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

                # run this game according to the defined rules and the player strategies for move choice
                data = run_game(player_one, player_two, game+1, args)
                end_time = time.time()
                data['init_marbles']  = init_marbles
                result_list.append(data)

                bar.next()

    return get_result().append(result_list)

# ====================================================================================================

def main(args):

    result = run_sims('min_max', 'min_max', args)

    output = f'data/{args.output}.csv'
    print(f'Saving output to {output}')
    result.to_csv(output, index=False)

# ====================================================================================================

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--ngames',
            default = 5000,
            type = int,
            help = 'Number of independent mancala games to run')

    parser.add_argument('-o', '--output',
            required = True,
            help = 'output file')

    parser.add_argument('--max-n-marbles',
            default = 20,
            type = int,
            help = 'Maximum number of initial marble number to consider')

    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'Verbose output')

    args = parser.parse_args()

    main(args)
