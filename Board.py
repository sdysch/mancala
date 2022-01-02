class Board:
    ''' Class which holds a representation of a Mancala board '''

    _NCUPS = 6

    def __init__(self):
        self.player_one_cups = self._NCUPS * [6]
        self.player_two_cups = self._NCUPS * [6]

        self.player_one_goal = 0
        self.player_two_goal = 0

    def __str__(self):
        '''
        format the board in a pretty string: 

                    6 6 6 6 6 6
            [0]                      [0]
                    6 6 6 6 6 6


        '''
        offset       = 5
        offset_space = 3

        board_string = (offset + offset_space) * ' ' + ' '.join([str(v) for v in self.player_two_cups])

        board_string += '\n'
        board_string += f'[{self.player_two_goal}]'
        board_string +=  2 * (offset + self._NCUPS ) * ' '
        board_string += f'[{self.player_one_goal}]'
        board_string += '\n'

        board_string += (offset + offset_space) * ' ' + ' '.join([str(v) for v in self.player_one_cups])
        return board_string
