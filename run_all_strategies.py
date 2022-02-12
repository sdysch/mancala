def main(args):

    from core.game.util import run_trials_of_different_agents

    all_strategies = [
            'random',
            'max_score',
            'exact_random',
            'exact_max_score',
            'max_marbles',
            'max_moves',
    ]

    player_one_strategies = all_strategies
    player_two_strategies = all_strategies

    result = run_trials_of_different_agents(player_one_strategies, player_two_strategies, args)

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
            default = 4,
            required = False,
            type = int,
            help = 'Number of initial marbles in buckets')

    parser.add_argument('-o', '--output',
            default = 'output', 
            type = str,
            help = 'Stamp for outputs')

    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'Verbose output')

    parser.add_argument('-p', '--parallel',
            default = False,
            action = 'store_true',
            help = 'Run jobs in parallel (multiprocess)')

    parser.add_argument('--max-workers',
            default = 4,
            type = int,
            help = 'Maximum number of parallel workers')

    parser.add_argument('-d', '--depth',
            default = 3,
            type = int,
            help = 'Max depth of min_max strategy')

    args = parser.parse_args()

    main(args)
