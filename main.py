def main(args):

    from Board import Board

    test_board = Board()
    print(test_board)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
