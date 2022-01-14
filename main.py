def main(args):

    from Board import Board

    board = Board()

    player       = 1
    start_side   = 1
    start_choice = 6

    # make initial move
    side, position = board.make_player_move(player, start_choice, start_side)

    while not board.no_more_moves():
        print(board)
        # ended in player goal - they get a new move
        if side == None and position == 0:
            moves = board.available_moves(player)
            # dummy strategy for now
            side, position = board.make_player_move(player, moves[0], player)

        # if the last marble was put into an empty bucket, the players switch
        elif board.last_bucket_empty(side, position):
            player = 1 if player == 2 else 2
            side_of_board = player
            moves = board.available_moves(player)
            # dummy strategy for now
            side, position = board.make_player_move(player, moves[0], side_of_board)

        # same player continues from the position the previous move terminated in
        else:
            side, position = board.make_player_move(player, position, side)
            
    print('\n' + 100 * '=')
    print(f'Final board layout:\n {board}')
    board.calculate_final_board_scores()

    print('\n' + 100 * '=')
    print(f'Player 1 score: {board.player_one_goal}')
    print(f'Player 2 score: {board.player_two_goal}')
    print(f'Player 1 moves: {board.n_moves_player_one}')
    print(f'Player 2 moves: {board.n_moves_player_two}')
    print(f'Total moves: {board.n_moves}')


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
