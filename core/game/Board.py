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

        self.n_moves_player_one = 0
        self.n_moves_player_two = 0

        # Note, a player can be moving marbles on the opponents side. Store these separately
        self.player = Board._INITIAL_PLAYER
        self.side   = Board._INITIAL_PLAYER

        self.position = None

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

    def make_player_move(self, player_number, bucket, side_of_board):
        """ Make a single move for player_number, starting from bucket number bucket on side_of_board """

        self.check_valid_player(player_number)
        self.check_valid_bucket(bucket)
        self.check_valid_side(side_of_board)

        # get the number of marbles from the chosen position, reset this bucket
        if side_of_board == 1:
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
        position = bucket + 1

        # whose cups we are updating
        updating_cups = side_of_board

        # flag to keep track if we ended in a player's goal
        ended_in_goal = False

        # distribute the marbles across the board
        for _ in range(marbles):
            # we have reached the edge of the board
            if position == self._NCUPS + 1:

                # if we have been iterating over the player's cups, update their goal
                # else, update the _initial_ cup of the other player
                if updating_cups == player_number:
                    ended_in_goal = True
                    position = 1
                    self.update_player_goal(player_number, 1)

                else:
                    position = 2
                    self.update_opponent_cups(updating_cups, 1, 1)

                # switch whose goal we are updating
                updating_cups = 1 if updating_cups == 2 else 2

            # not yet reached the end of the board
            else:
                self.update_player_cups(updating_cups, position, 1)
                ended_in_goal = False
                position += 1


        # store the side of the board we ended on (1 or 2), and the bucket we ended on
        # if we ended in the player's goal (ended_in_goal==True), store position of 0, updating_cups None
        if ended_in_goal:
            position = 0
            updating_cups = None

        # need to subtract 1 from position, as we have incremented the position once too many inside the for loop
        elif position == 1:
            updating_cups = 1 if updating_cups == 2 else 2
            position = self._NCUPS

        else:
            position -= 1

        self.side     = updating_cups
        self.position = position

    def no_more_moves(self):
        ''' returns True if there are no more moves (one side of the board is empty) else False '''
        return ( not any(self.player_one_cups) or not any(self.player_two_cups) )
    
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

    def last_bucket_empty(self, side, position):
        ''' returns True if the bucket at position-1 was empty before this move finished '''

        self.check_valid_bucket(position)
        self.check_valid_side(side)

        if position == 0:
            raise ValueError('Position == 0 means that the previous move ended in a player goal. Please check your logic')

        # ended in position 1 - we need to check buckets on previous side
        elif position == 1:
            new_side = 1 if side == 2 else 2
            cups = self.get_player_cups(new_side)
            if cups[self._NCUPS - 1] == 1:
                return True
            else:
                return False

        else:
            buckets = self.get_player_cups(side)
            if buckets[position - 1] == 1:
                return True
            else:
                return False

    def calculate_final_board_scores(self):
        ''' calculates the final player scores '''

        if not self.no_more_moves():
            print(f'There are still valid moves on the board:\n{self}')
            return
        
        # add the remaining marbles to the goal of the player who emptied their side
        if any(self.player_two_cups):
            self.player_one_goal += sum(self.player_two_cups)
            self.player_two_cups = [0 for _ in self.player_two_cups]
        else:
            self.player_two_goal += sum(self.player_one_cups)
            self.player_one_cups = [0 for _ in self.player_one_cups]

    def run_full_game(self, player_one, player_two):
        """
            Runs the mancala game from the current board state.
            player_one and player_two are of the type core.players.Player, and control the move selection strategy
        """

        if self.player == 1:
            self.position = player_one.move(self)
        else:
            self.position = player_two.move(self)

        # store initial move choice
        self.first_move = self.position

        # make initial move
        self.make_player_move(self.player, self.position, self.side)

        while not self.no_more_moves():
            self.make_player_turn(player_one, player_two)

    def make_player_turn(self, player_one, player_two):
        """ Wrapper around make_player_move to run a move choice for a player,
            implementing the mancala rules """

            # TODO add tests for this in tests/test_board.py

        # ended in player goal - they get a new move
        if self.side == None and self.position == 0:
            move = player_one.move(self) if self.player == 1 else player_two.move(self)
            self.make_player_move(self.player, move, self.player)

        # if the last marble was put into an empty bucket, the players switch
        elif self.last_bucket_empty(self.side, self.position):
            self.player = 1 if self.player == 2 else 2
            self.side = self.player
            move = player_one.move(self) if self.player == 1 else player_two.move(self)
            self.make_player_move(self.player, move, self.player)

        # same player continues from the position the previous move terminated in
        else:
            self.make_player_move(self.player, self.position, self.side)
