class Board:
    ''' Class which holds a representation of a Mancala board '''

    _INITIAL_PLAYER = 1

    def __init__(self, *args, **kwargs):

        self._N_MARBLES      = kwargs.get('n_start_marbles', 6)
        self._NCUPS          = kwargs.get('n_cups', 6)

        self.player_one_cups = self._NCUPS * [self._N_MARBLES]
        self.player_two_cups = self._NCUPS * [self._N_MARBLES]

        self.player_one_goal = 0
        self.player_two_goal = 0

        # counter to keep track of how many moves (choices) a player makes
        self.n_moves_player_one = 0
        self.n_moves_player_two = 0

        # Note, a player can be moving marbles on the opponents side. Store these separately
        self.player = Board._INITIAL_PLAYER
        self.side   = Board._INITIAL_PLAYER

        self.position = None

        self.half_marbles_rule = False

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
        """ Returns True if self and other have the same board layout, and False if not """
        if self.player_one_goal == other.player_one_goal \
        and self.player_two_goal == other.player_two_goal \
        and self.player_one_cups == other.player_one_cups \
        and self.player_two_cups == other.player_two_cups \
        and self.side == other.side \
        and self.player == other.player:
            return True
        else:
            return False

    @property
    def n_moves(self):
        return self.n_moves_player_one + self.n_moves_player_two
    
    @property
    def sum_player_goals(self):
        return self.player_one_goal + self.player_two_goal

    def check_valid_player(self, player_number):
        ''' Check if player number is valid '''

        if player_number not in [1, 2]:
            raise ValueError(f'Player number must be either 1 or 2. Value {player_number} is invalid')

    def check_valid_side(self, side):
        ''' Check if side number is valid '''

        if side not in [1, 2]:
            raise ValueError('Side must be either 1 or 2')

    def check_valid_bucket(self, bucket):
        ''' Check if chosen bucket is valid '''

        if not (bucket >= 1 and bucket <= self._NCUPS):
            raise ValueError(f'Invalid bucket number "{bucket}"')

    def get_player_cups(self, player_number):
        ''' get the cups for player_number '''

        self.check_valid_player(player_number)
        return self.player_two_cups if player_number == 2 else self.player_one_cups

    def get_opponent_cups(self, player_number):
        ''' get the cups for opponent '''

        self.check_valid_player(player_number)
        return self.player_one_cups if player_number == 2 else self.player_two_cups

    def update_player_cups(self, player_number, bucket, value):
        ''' update the player_number's bucket with value '''

        self.check_valid_player(player_number)
        self.check_valid_bucket(bucket)

        if player_number == 1:
            self.player_one_cups[bucket - 1] += value
        else:
            self.player_two_cups[bucket - 1] += value

    def update_opponent_cups(self, player_number, bucket, value):
        if player_number == 1:
            return self.update_player_cups(2, bucket, value)
        elif player_number == 2:
            return self.update_player_cups(1, bucket, value)
        else:
            raise ValueError(f'Invalid player number {player_number}')

    def get_player_goal(self, player_number):
        ''' get the goal for player_number '''

        self.check_valid_player(player_number)
        player_goal = self.player_one_goal if player_number == 1 else self.player_two_goal

        return player_goal

    def get_opponent_goal(self, player_number):
        ''' get the goal for opponent_number '''

        self.check_valid_player(player_number)
        opponent_goal = self.player_one_goal if player_number == 2 else self.player_two_goal

        return opponent_goal

    def update_player_goal(self, player_number, value):
        ''' update the goal for player_number with value'''

        self.check_valid_player(player_number)
        if player_number == 1:
            self.player_one_goal += value
        else:
            self.player_two_goal += value

    def calculate_final_board_scores(self):
        ''' calculates the final player scores '''

        if not self.no_more_moves():
            print(f'There are still valid moves on the board:\n{self}')
            return
        
        # add the remaining marbles to each player's goal
        self.player_one_goal += sum(self.player_one_cups)
        self.player_one_cups = [0 for _ in self.player_one_cups]

        self.player_two_goal += sum(self.player_two_cups)
        self.player_two_cups = [0 for _ in self.player_two_cups]

    def run_full_game(self, player_one, player_two, verbose=False):
        """
            Runs the mancala game from the current board state.
            player_one and player_two are of the type core.players.Player, and control the move selection strategy
        """

        if self.player == 1:
            player = player_one
        else:
            player = player_two

        # store initial move choice
        self.position = self.first_move
        self.first_move = self.position
        self.iterate_until_turn_over(player, self.position, verbose)

        while not self.no_more_moves():
            player = player_one if self.player == 1 else player_two
            move = player.move(self)
            self.iterate_until_turn_over(player, move, verbose)

    def iterate_until_turn_over(self, player, initial_move, verbose=False):
        """ Iterate board, implementing mancala rules, until the players switch.
            I.e. until the players switch """

        # TODO add tests for this in tests/test_board.py

        # make initial move
        self.make_player_move(self.player, initial_move, self.side)

        turn_over = True if self.no_more_moves() else False
        while not turn_over:
            if verbose:
                print(self)

            # ended in player goal - they get a new move
            if self.side == None and self.position == 0:
                if self.no_more_moves():
                    turn_over = True
                else:
                    move = player.move(self)
                    self.make_player_move(self.player, move, self.player)

            # didn't end in player goal, check if player's turn is over and continue iterating if not
            else:
                if self.last_bucket_empty():
                    turn_over = True
                else:
                    self.make_player_move(self.player, self.position, self.side)
        # swap players
        self.player = 1 if self.player == 2 else 2
        self.side = self.player
        return

    def make_player_move(self, player_number, bucket, side):
        """ Make a single move for player_number, starting from bucket number bucket on side_of_board """

        self.check_valid_player(player_number)
        self.check_valid_bucket(bucket)
        self.check_valid_side(side)

        # get the number of marbles from the chosen position, reset this bucket
        if side == 1:
            marbles = self.player_one_cups[bucket - 1]
            self.player_one_cups[bucket - 1] = 0

        else:
            marbles = self.player_two_cups[bucket - 1]
            self.player_two_cups[bucket - 1] = 0

        # if there are no marbles, this is not a valid move and we return
        if marbles == 0:
            raise ValueError('A bucket with 0 marbles was chosen. This is invalid.')

        # passed all validity checks - this is a valid move, so increment counters
        if player_number == 1:
            self.n_moves_player_one += 1

        elif player_number == 2:
            self.n_moves_player_two += 1

        # starting position
        self.position = bucket + 1

        # whose cups we are updating
        self.side = side

        # flag to keep track if we ended in a player's goal
        ended_in_goal = False

        # distribute the marbles across the board
        for _ in range(marbles):
            # we have reached the edge of the board
            if self.position == self._NCUPS + 1:

                # if we have been iterating over the player's cups, update their goal
                # else, update the _initial_ cup of the other player
                if self.side == player_number:
                    ended_in_goal = True
                    self.position = 1
                    self.update_player_goal(player_number, 1)

                else:
                    self.position = 2
                    self.update_opponent_cups(self.side, 1, 1)

                # switch side
                self.side = 1 if self.side == 2 else 2

            # not yet reached the end of the board
            else:
                self.update_player_cups(self.side, self.position, 1)
                ended_in_goal = False
                self.position += 1


        # store the side of the board we ended on (1 or 2), and the bucket we ended on
        # if we ended in the player's goal (ended_in_goal==True), store position of 0, updating_cups None
        if ended_in_goal:
            self.position = 0
            self.side = None

        # need to subtract 1 from position, as we have incremented the position once too many inside the for loop
        elif self.position == 1:
            self.side = 1 if self.side == 2 else 2
            self.position = self._NCUPS

        else:
            self.position -= 1

    def no_more_moves(self):
        """ returns True if there are no more moves:
            * one side of the board is empty
            * more than half the marbles have been captured
        If not, returns False """

        if not any(self.player_one_cups) or not any(self.player_two_cups):
            return True
        if self.half_marbles_rule:
            if self.sum_player_goals >= 0.5 * self._N_MARBLES * self._NCUPS:
                return True
        return False
    
    def available_moves(self, player):
        ''' returns a list of valid moves for this player '''
        self.check_valid_player(player)

        if self.no_more_moves():
            return []

        buckets = self.get_player_cups(player)
        buckets_with_marbles = []
        for i, bucket in enumerate(buckets):
            if bucket != 0:
                buckets_with_marbles.append(i+1)
        return buckets_with_marbles

    def last_bucket_empty(self):
        ''' returns True if the bucket at position-1 was empty before this move finished.
            I.e., the last move played ended in an empty goal'''

        if self.position == 0:
            raise ValueError('Position == 0 means that the previous move ended in a player goal. Please check your logic')

        # ended in position 1 - we need to check buckets on previous side
        elif self.position == 1:
            new_side = 1 if self.side == 2 else 2
            cups = self.get_player_cups(new_side)
            if cups[self._NCUPS - 1] == 1:
                return True
            else:
                return False

        else:
            buckets = self.get_player_cups(self.side)
            if buckets[self.position - 1] == 1:
                return True
            else:
                return False

