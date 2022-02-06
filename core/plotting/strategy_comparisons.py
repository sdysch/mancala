# ====================================================================================================

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ====================================================================================================

def calculate_prob(data, column, value):
    return len(data[data[column] == value]) / len(data)

# ====================================================================================================

def make_prob_matrix(data, title, savename):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    cmap = sns.color_palette("light:b", as_cmap=True)
    sns.heatmap(data, annot=True, linewidths=0.5, ax=ax, cmap=cmap, square=True)

    ax.set_xlabel('player 1 strategy', fontsize=16)
    ax.set_xticklabels(data.columns, rotation=45)

    ax.set_ylabel('player 2 strategy', fontsize=16)
    #ax.set_yticklabels(data.index, rotation=65)

    ax.set_title(title, fontsize=16)

    plt.savefig(f'{savename}.pdf')
    plt.savefig(f'{savename}.png')

# ====================================================================================================

def main(args):
    df = pd.read_csv(args.input)

    all_strategies = [
            'random',
            'max_score',
            'exact_random',
            'exact_max_score',
            'max_marbles',
    ]

    player_1_win_probs = pd.DataFrame(columns=all_strategies, index=all_strategies, dtype='float')
    draw_probs         = pd.DataFrame(columns=all_strategies, index=all_strategies, dtype='float')
    player_2_win_probs = pd.DataFrame(columns=all_strategies, index=all_strategies, dtype='float')
    for player_1_strat in all_strategies:
        for player_2_strat in all_strategies:
            reduced_df = df[ (df['player_one_strategy'] == player_1_strat) & (df['player_two_strategy'] == player_2_strat) ]

            player_1_win_probs[player_1_strat].loc[player_2_strat] = calculate_prob(reduced_df, 'player_1_result', 'win')
            player_2_win_probs[player_1_strat].loc[player_2_strat] = calculate_prob(reduced_df, 'player_2_result', 'win')
            draw_probs[player_1_strat].loc[player_2_strat]         = calculate_prob(reduced_df, 'player_1_result', 'draw')

    #print(player_1_win_probs.to_numpy())
    make_prob_matrix(player_1_win_probs, 'Player 1 win probability', 'plots/player_1_win_probs')
    make_prob_matrix(player_2_win_probs, 'Player 2 win probability', 'plots/player_2_win_probs')
    make_prob_matrix(draw_probs, 'Draw probability', 'plots/draw_probability')

# ====================================================================================================

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
            default = 'data/all_simulations.csv', 
            type = str,
            help = 'input file')

    args = parser.parse_args()

    main(args)
