class Board:
    ''' Class which holds a representation of a Mancala board '''

    def __init__(self, *args, **kwargs):

        self.n_start_marbles = kwargs.get('n_start_marbles', 6)
        self._NCUPS          = kwargs.get('n_cups',          6)

        self.player_one_cups = self._NCUPS * [self.n_start_marbles]
        self.player_two_cups = self._NCUPS * [self.n_start_marbles]

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

        board_string += '\n'

        return board_string

    def __eq__(self, other):
        if self.player_one_goal == other.player_one_goal \
        and self.player_two_goal == other.player_two_goal \
        and self.player_one_cups == other.player_one_cups \
        and self.player_two_cups == other.player_two_cups:
            return True
        else:
            return False

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
        if player_number == 1:
            marbles = self.player_one_cups[bucket - 1]
            self.player_one_cups[bucket - 1] = 0
        else:
            marbles = self.player_two_cups[bucket - 1]
            self.player_two_cups[bucket - 1] = 0

        # if there are no marbles, this is not a valid move and we return
        if marbles == 0:
            return

        # starting position
        # if bucket == self._NCUPS:
            # position = self._NCUPS
        # else:
            # position = bucket + 1
        position = bucket + 1

        # whose cups we are updating
        original_player = player_number
        updating_cups   = player_number

        # flag to keep track if we ended in a player's goal
        ended_in_goal = False

        # distribute the marbles across the board
        for _ in range(marbles):
            # print(self)
            # print(position)
            # we have reached the edge of the board
            if position == self._NCUPS + 1:
                # only update player's goal if we have been iterating over their cups
                # otherwise, we need to update the initial cup of the other player
                if updating_cups == original_player:
                    ended_in_goal = True
                    position = 1
                    if updating_cups == 1:
                        self.player_one_goal += 1
                    else:
                        self.player_two_goal += 1

                else:
                    position = 2
                    if updating_cups == 1:
                        self.player_two_cups[0] += 1
                    else:
                        self.player_one_cups[0] += 1

                # switch whose goal we are updating
                updating_cups = 1 if updating_cups == 2 else 2

            # not yet reached the end of the board
            else:
                if updating_cups == 1:
                    self.player_one_cups[position - 1] += 1
                else:
                    self.player_two_cups[position - 1] += 1

                # update position for next turn
                ended_in_goal = False
                position += 1

        return ended_in_goal
