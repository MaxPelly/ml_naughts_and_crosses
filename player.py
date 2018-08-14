import re
from nn import Neural_Net
import numpy as np


class BasePlayer(object):
    """
    Base player class with function stubs for inheriting from, should ensure any player is usable and wont crash and for
    IDE autocomplete
    """
    
    def __init__(self):
        """
        creates a new player, sets moved illegally to false to allow tracking of illegal moves
        this will be set to true by the board if an illegal move is made
        """
        
        self.moved_illegally = False
        
    def play(self, state, player_number):
        """
        a function stub to be called by the board to get the players move
        :param state: the current state of the board
        :param player_number: the player's player number, assigned by the board
        :return: an (x,y) coordinate of the players move
        """
        
        print("Function stub, please override")
        return 0, 0

    def results(self, winner, player_number):
        """
        a function stub to allow the player to respond to the games result, printing a congratulatory message etc...
        :param winner: the winning player object
        :param player_number: the player's player number, assigned by the board
        :return: None
        """
        
        pass
        

class HumanPlayer(BasePlayer):
    """
    an extension of the base player class to implement a human player, asks for input using the command line and
    displays the relevant message after the game
    """
    
    def __init__(self):
        """
        generates a regex to check inout validity and extract move from any surrounding braces 
        """
        
        super().__init__()
        self.move_checker = re.compile('[0-2],[0-2]')

    def play(self, state, player_number):
        """
        diplays which players turn it is and the board, asks the player to pick a spot to move and verifies that this 
        is a possible move (on the oard), does not verify if the space is available
        :param state: the current state of the board
        :param player_number: the player's player number, assigned by the board
        :return: an (x,y) coordinate of the players move
        """
        
        print('Player {}\'s turn'.format(player_number))
        self._display(state)
        while True:
            print()
            move = input('Where woud you like to go? [x,y] >>> ')
            match = self.move_checker.search(move)
            if match:
                pos_str = match.group(0)
                pos = pos_str.split(',')

                return [int(i) for i in pos]
            else:
                print(f'"{move}" is not a valid move, please enter two numbers (0 - 2) separated by a coma')

    def results(self, winner, player_number):
        """
        prints a message depending on the result to let the player know if they won
        :param winner: the winning player object
        :param player_number: the player's player number, assigned by the board
        :return: None
        """
        if winner == self:
            print(f"Player {player_number} wins!!!!!")
        elif winner:
            print(f"Player {player_number} lost")
        else:
            print("Tie")

    @staticmethod
    def _display(state):
        """
        an internal method to display the board on the command line
        :param state: the current state of the board
        :return: None
        """
        for y in range(3):
            out_str = '|'
            for x in range(3):
                out_str += f'{state[x][y]}|'
            print(out_str)
        print()


class NNPlayer(BasePlayer):
    def __init__(self, net_shape=(9, 18, 9, 9)):
        super().__init__()
        self.brain = Neural_Net(net_shape)
        self.elo = 1000

    def play(self, state, player_number):
        state = np.array(state)
        tensor = state.reshape((9,1))
        guess_tensor = self.brain.feed_forward(tensor)
        guess = guess_tensor.reshape((3, 3))

        max = -np.inf
        for x in (0, 1, 2):
            for y in (0, 1, 2):
                if guess[x,y] > max:
                    max = guess[x,y]
                    max_x = x
                    max_y = y
        return max_x, max_y
    
    @staticmethod
    def update_elo(winner, loser, tie=False):
        pass


if __name__ == '__main__':
    bot = NNPlayer()
    print(bot.play(((1,2,3), (4,5,6),(7,8,9))))
