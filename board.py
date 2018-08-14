class Board (object):
    """
    The board on which the game is played, deals with player management, turn tracking and win condition.
    players should be objects with a play function accepting the current state of the board and return a tuple (x,y)
    of where they want to play

    also handles move validity checking though will not communicate bad moves to the player, they should also check first
    """

    def __init__(self, player_one, player_two):
        """
        creates a new board
        :param player_one: the first player, an object implementing a play function
        :param player_two: the first player, an object implementing a play function
        """

        self.state = [[0 for _ in range(3)] for _ in range(3)]
        self.won = False
        self.winner = None
        self.player_one = player_one
        self.player_two = player_two
        
    def get(self, pos):
        """
        gets the state of the bored at pos (x,y)
        :param pos: the x,y coordinates of the piece to get
        :return: the state of the board. (0: un owned, 1, owned by player 1, 2: owned by player 2)
        """

        return self.state[pos[0]][pos[1]]
        
    def set(self, pos, val):
        """
        sets the state of the board at pos (x,y) to val, no error checking, assumes move is valid
        :param pos: the (x,y) coordinates of the position to set
        :param val: the value to set the board to. (0: un owned, 1, owned by player 1, 2: owned by player 2)
        :return: None
        """

        self.state[pos[0]][pos[1]] = val

    def play(self):
        """
        the main loop, plays a game by asking each player in turn for their move (passing them the bord state) and then
        checking the win condition
        performs move validity checking though if an invalid move is detected the player is simply skipped
        :return:
        """

        current_player, next_player = self.player_one, self.player_two
        current_id = 1
        while not self.won:
            pos = current_player.play(state=self.state, player_number=current_id)
            if self._check_move_legality(pos):
                # todo implement some sort of illegal move penalty
                pass
            else:
                self.set(pos, current_id)
            self._test_for_win(pos)
            current_player, next_player = next_player, current_player
            current_id = current_id % 2 + 1
            print(self.won)

    def _check_move_legality(self, pos):
        """
        checks if a proposed move uis legal.
        Checks:
            the move is a tuple or list
            the space exists on the board
            the proposed position is not already claimed
        :param pos:
        :return: True if the move is legal, otherwise false
        """

        if type(pos) not in (tuple, list) or\
                pos[0] not in (0, 1, 2) or pos[1] not in (0, 1, 2) or \
                self.get(pos) != 0:
            return False
        return True

    def _test_for_win(self, pos):
        """
        Checks for a win following a move at pos (x,y) and sets self.won accordingly
        assumes noone has previously won
        currently dosent check diagonals
        :param pos:
        :return: None
        """

        # todo implement diagonals
        player = self.get(pos)
        x, y = pos
        to_check = ((1, 2), (-1, 1), (-1, -2))
        check_x = to_check[x]
        check_y = to_check[y]
        self.won = (player == self.get((x + check_x[0], y)) and player == self.get((x + check_x[1], y))) or \
                   (player == self.get((x, y + check_y[0])) and player == self.get((x, y + check_y[1])))


# play a game with two human players for debugging purposes
if __name__ == '__main__':
    from player import HumanPlayer
    player_one, player_two = (HumanPlayer() for _ in range(2))
    board = Board(player_one, player_two)
    board.play()
                

