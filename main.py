def main(args):

    from Board import Board

    board = Board()

    print(board.available_moves(1))

    choice = 6
    player = 1
    side_of_board = 1
    while board.no_more_moves():
        side, position = board.make_player_move(player, choice, side_of_board)

        # first, check that we didn't finish the game
        if board.no_more_moves():
            break

        # ended in player goal - they get a new move
        if side == None and position == 0:
            moves = board.available_moves(player)
            # dummy strategy for now
            board.make_player_move(player, moves[0], player)

        # check if the last marble was put into an empty bucket
        elif board.last_bucket_empty(side, position)

        # next players move
        else:
            if player == 1:
                player = 2:
            else
                player = 1



if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
