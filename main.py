def main(args):

    from Board import Board

    test_board = Board()
    #print(test_board)

    # test_board.player_one_cups = [0, 0, 0, 0, 0, 6]
    # test_board.player_two_cups = [0, 0, 0, 0, 0, 0]
    # print(test_board)
    # test_board.make_player_move(1, 6)
    # print(test_board)

    #test_board.player_two_cups = [0, 0, 0, 0, 0, 7]
    #test_board.player_two_cups = [0, 0, 0, 0, 0, 9]
    #test_board.player_one_cups = [0, 0, 5, 0, 0, 0]
    #print(test_board)
    #test_board.make_player_move(1, 3)
    #test_board.make_player_move(2, 6)
    #print(test_board)

    print(test_board)
    if test_board.no_more_moves():
        print('No more moves')

    test_board.player_one_cups = [0, 0, 0, 0, 0, 0]
    print(test_board)
    if test_board.no_more_moves():
        print('No more moves')

    test_board.player_one_cups = [1, 2, 3, 4, 0, 0]
    test_board.player_two_cups = [0, 0, 0, 0, 0, 0]
    print(test_board)
    if test_board.no_more_moves():
        print('No more moves')

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
