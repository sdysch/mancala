def main(args):

    from Board import Board

    test_board = Board()
    #print(test_board)

    test_board.player_one_cups = [7, 0, 0, 0, 0, 0]
    test_board.player_two_cups = [1, 0, 0, 0, 0, 0]
    print(test_board)
    test_board.make_player_move(1, 1)
    print(test_board)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
