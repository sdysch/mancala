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

        # player two cups are numbered right to left, so we reverse the list when printing
        temp_player_two_cups = self.player_two_cups
        temp_player_two_cups.reverse()
        board_string = (offset + offset_space) * ' ' + ' '.join([str(v) for v in temp_player_two_cups])

        board_string += '\n'
        board_string += f'[{self.player_two_goal}]'
        board_string +=  2 * (offset + self._NCUPS ) * ' '
        board_string += f'[{self.player_one_goal}]'
        board_string += '\n'

        board_string += (offset + offset_space) * ' ' + ' '.join([str(v) for v in self.player_one_cups])

        return board_string

    def check_valid_player(self, player_number):
        ''' Check is player number is valid '''

        if player_number not in [1, 2]:
            raise ValueError('Player number must be either 1 or 2')

    def check_valid_bucket(self, bucket):
        ''' Check if chosen bucket is valid '''

        valid_buckets = [v + 1 for v in range(self._NCUPS)]
        if bucket not in [valid_buckets]:
            raise ValueError('Invalid bucket number')

    def get_player_cups(self, player_number):
        ''' get the cups for player_number '''

        self.check_valid_player(player_number)
        return self.player_two_cups if player_number == 2 else self.player_one_cups

    def get_opponent_cups(self, player_number):
        ''' get the cups for opponent '''

        self.check_valid_player(player_number)
        return self.player_one_cups if player_number == 2 else self.player_two_cups

    def get_player_goal(self, player_number):
        ''' get the goal for player_number '''

        self.check_valid_player(player_number)
        player_goal = self.player_one_goal if player_number == 1 else self.player_two_goal

        return player_goal

    def is_valid_move(self, player_number, bucket):
        ''' Checks if a player's bucket has at least 1 marble in it, therefore enabling a valid move '''

        self.check_valid_player(player_number)
        self.check_valid_bucket(bucket)

        player_cups = self.get_player_cups

        return player_cups[bucket - 1] == 0

    def make_player_move(self, player_number, bucket):
        ''' Iterate through board until no valid moves are left '''

        if not self.is_valid_move(player_number, bucket):
            return

        self.check_valid_player(player_number)
        self.check_valid_bucket(bucket)

        if player_number == 1:
            player_cups   = self.player_one_cups
            opponent_cups = self.player_two_cups
        else:
            player_cups   = self.player_two_cups
            opponent_cups = self.player_one_cups

        marbles = player_cups[bucket - 1]
        player_cups[bucket - 1] = 0

