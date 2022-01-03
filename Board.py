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
        # deep copy, because we do not want to actually reverse the list in place
        temp_player_two_cups = [v for v in self.player_two_cups]
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

        if not (bucket >= 1 and bucket <= self._NCUPS):
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

    def get_opponent_goal(self, player_number):
        ''' get the goal for opponent_number '''

        self.check_valid_player(player_number)
        opponent_goal = self.player_one_goal if player_number == 1 else self.player_two_goal

        return opponent_goal

    def make_player_move(self, player_number, bucket):
        ''' Iterate through board until valid moves are left '''

        self.check_valid_player(player_number)
        self.check_valid_bucket(bucket)

        # get player/opponent cups and goals
        player_cups   = self.get_player_cups(player_number)

        # if there are no marbles, this is not a valid move and we return
        marbles = player_cups[bucket - 1]
        if marbles == 0:
            return

        opponent_cups = self.get_opponent_cups(player_number)
        player_goal   = self.get_player_goal(player_number)
        opponent_goal = self.get_opponent_goal(player_number)

        # starting position
        position = bucket

        # reset this bucket to 0
        player_cups[bucket - 1] = 0

        # whose cups we are updating
        updating_cups = player_number

        # flag to keep track if we ended in a player's goal
        ended_in_goal = False

        # distribute the marbles across the board
        for _ in range(marbles):

            # we have reached the edge of the board
            if position == self._NCUPS:
                player_goal += 1

                # now we are at the edge of the board, switch whose goal we are updating
                updating_cups = 1 if updating_cups == 2 else 2

                # reset position for next player
                ended_in_goal = True
                position = 0

            else:
                ended_in_goal = False
                position += 1

                if updating_cups == 1:
                    player_cups[position - 1] += 1
                elif updating_cups == 2:
                    opponent_cups[position - 1] += 1
                else:
                    raise ValueError('updating_cups is neither 1 nor 2, this should not happen')

        # store the updated player and opponent cups/goals
        self.player_one_cups = player_cups
        self.player_two_cups = opponent_cups

        self.player_one_goal = player_goal
        self.player_two_goal = opponent_goal

        return ended_in_goal
