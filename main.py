def main(args):

    from Board import Board

    test_board = Board()
    print(test_board)

    test_board.player_two_cups = [0, 1, 2, 3, 4, 5]
    print(test_board)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
