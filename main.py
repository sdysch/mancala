def main(args):

    from Board import Board

    test_board = Board()
    print(test_board)

    #ended_in_goal = test_board.make_player_move(1, 1)
    ended_in_goal = test_board.make_player_move(1, 2)
    if (ended_in_goal):
        print('Ended in goal')

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
