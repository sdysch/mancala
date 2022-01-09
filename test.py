def main(args):

    from Board import Board

    board = Board()
    board.player_one_cups = [0, 0, 0, 0, 3, 0]
    board.player_two_cups = [0, 0, 0, 0, 4, 0]

    print(board)
    side, position = board.make_player_move(1, 5, 1)
    print(position)
    print(board.last_bucket_empty(side, position))

    print(board)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
