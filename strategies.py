def main(args):

    from core.game.util import run_trials

    result = run_trials(args)

    output = f'data/{args.output}.csv'
    print(f'Saving output to {output}')
    result.to_csv(output, index=False)

# ====================================================================================================

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--ngames',
            default = 10000,
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

    parser.add_argument('--make-runtime-plots',
            default = True,
            type = bool,
            help = 'Plot runtime vs number of games simulated')

    parser.add_argument('--save-runtime-list',
            default = True,
            type = bool,
            help = 'Pickle list of runtime vs n_games')

    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'Verbose output')

    args = parser.parse_args()

    main(args)
