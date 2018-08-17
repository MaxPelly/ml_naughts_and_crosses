from player import BasePlayer


class Board (object):
    """
    The board on which the game is played, deals with player management, turn tracking and win condition.
    players should be objects with a play function accepting the current state of the board and return a tuple (x,y)
    of where they want to play

    also handles move validity checking though will not communicate bad moves to the player, just mark and skip
    they should also check first
    """

    def __init__(self, player_one, player_two):
        """
        creates a new board
        :param player_one: the first player, an object implementing a play function
        :type player_one: BasePlayer
        :param player_two: the first player, an object implementing a play function
        :type player_two: BasePlayer
        """

        self.state = [[0 for _ in range(3)] for _ in range(3)]
        self.won = False
        self.winner = None
        self.player_one = player_one  # type: BasePlayer
        self.player_two = player_two  # type: BasePlayer
        
    def get(self, pos):
        """
        gets the state of the bored at pos (x,y)
        :param pos: the x,y coordinates of the piece to get
        :type pos: int[2]
        :return: the state of the board. (0: un owned, 1, owned by player 1, 2: owned by player 2)
        :rtype: int
        """

        return self.state[pos[0]][pos[1]]
        
    def set(self, pos, val):
        """
        sets the state of the board at pos (x,y) to val, no error checking, assumes move is valid
        :param pos: the (x,y) coordinates of the position to set
        :type pos: int[2]
        :param val: the value to set the board to. (0: un owned, 1, owned by player 1, 2: owned by player 2)
        :type val: int
        """

        self.state[pos[0]][pos[1]] = val

    def play(self):
        """
        the main loop, plays a game by asking each player in turn for their move (passing them the bord state) and then
        checking the win condition
        performs move validity checking though if an invalid move is detected the player is simply skipped
        """

        current_player, next_player = self.player_one, self.player_two
        current_id = 1
        play_count = 0
        last_player_played = True

        while not self.won and play_count < 9:
            pos = current_player.play(state=self.state, player_number=current_id)
            if self._check_move_legality(pos):
                self.set(pos, current_id)
                play_count += 1
                last_player_played = True
            else:
                current_player.moved_illegally = True
                if not last_player_played:
                    break
                last_player_played = False
            self._test_for_win(pos, current_id)
            current_player, next_player = next_player, current_player
            current_id = current_id % 2 + 1

        if self.won:
            # the winner must be the player that just went, as the players are swapped before braking the winning
            # payer will now be in the next player variable
            self.winner = next_player
        self.player_one.results(self.winner, 1)
        self.player_two.results(self.winner, 2)

        return next_player, current_player, not self.won  # returned for neural net training

    def _check_move_legality(self, pos):
        """
        checks if a proposed move uis legal.
        Checks:
            the move is a tuple or list
            the space exists on the board
            the proposed position is not already claimed
        :param pos: the position of the proposed move
        :type pos: int[2]
        :return: True if the move is legal, otherwise false
        :rtype: bool
        """

        if type(pos) not in (tuple, list) or\
                pos[0] not in (0, 1, 2) or pos[1] not in (0, 1, 2) or \
                self.get(pos) != 0:
            return False
        return True

    def _test_for_win(self, pos, player):
        """
        Checks for a win following a move at pos (x,y) and sets self.won accordingly
        assumes no one has previously won
        :param pos: the position of the last move
        :type pos: int[2]
        """

        x, y = pos
        to_check = ((1, 2), (-1, 1), (-1, -2))
        check_x = to_check[x]
        check_y = to_check[y]
        self.won = (player == self.get((x + check_x[0], y)) and player == self.get((x + check_x[1], y))) or \
                   (player == self.get((x, y + check_y[0])) and player == self.get((x, y + check_y[1]))) or \
                   (x == y and
                    player == self.get((0, 0)) and player == self.get((1, 1)) and player == self.get((2, 2))) or \
                   (x + y == 2 and
                    player == self.get((0, 2)) and player == self.get((1, 1)) and player == self.get((2, 0)))


if __name__ == '__main__':
    from player import HumanPlayer, NNPlayer
    one = HumanPlayer()
    two = NNPlayer()

    b = Board(one, two)
    b.play()
