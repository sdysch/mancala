def main(args):

    from core.game.util import run_sims

    if args.n_marbles is not None and args.n_marbles > 0:
        print(f'Setting initial number of marbles to {args.n_marbles}')

    result = run_sims(args.player_one_strategy, args.player_two_strategy, args)

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

    parser.add_argument('--n-marbles',
            required = False,
            type = int,
            help = 'Number of initial marbles in buckets')

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

    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'Verbose output')

    parser.add_argument('-d', '--depth',
            default = 3,
            type = int,
            help = 'Max depth of min_max strategy')

    args = parser.parse_args()

    main(args)
