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
        :type state: int[3][3]
        :param player_number: the player's player number, assigned by the board
        :type player_number: int
        :return: an (x,y) coordinate of the players move
        :rtype: int[2]
        """
        
        print("Function stub, please override")
        return 0, 0

    def results(self, winner, player_number):
        """
        a function stub to allow the player to respond to the games result, printing a congratulatory message etc...
        :param winner: the winning player object
        :type winner: BasePlayer
        :param player_number: the player's player number, assigned by the board
        :type player_number: int
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
        :type state: int[3][3]
        :param player_number: the player's player number, assigned by the board
        :type player_number: int
        :return: an (x,y) coordinate of the players move
        :rtype: int[2]
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
        :type winner: BasePlayer
        :param player_number: the player's player number, assigned by the board
        :type player_number: int
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
        :type state: int[3][3]
        """

        for y in range(3):
            out_str = '|'
            for x in range(3):
                out_str += f'{state[x][y]}|'
            print(out_str)
        print()


class NNPlayer(BasePlayer):
    """
    an extension of the BasePlayer class implementing a neural net powered bot. The bot also has a fitness
    and related functions to allow for training
    """

    def __init__(self, net_shape=(9, 18, 9, 9)):
        """
        makes a new neural net player
        :param net_shape: the shape of the players neural net
        :type net_shape: tuple
        """

        super().__init__()
        self.brain = Neural_Net(net_shape)  # type: Neural_Net
        self.elo = 1000

    def play(self, state, player_number):
        """
        passes the boards state to the neural net and attempts to play on the highest return value
        :param state: the current state of the board
        :type state: int[3][3]
        :param player_number: the player's player number, assigned by the board
        :type player_number: int
        :return: an (x,y) coordinate of the players move
        :rtype: int[2]
        """

        # todo make player number agnostic

        state = np.array(state)
        tensor = state.reshape((9, 1))
        guess_tensor = self.brain.feed_forward(tensor)
        guess = guess_tensor.reshape((3, 3))

        max_output, max_x, max_y = -np.inf, 0, 0
        for x in (0, 1, 2):
            for y in (0, 1, 2):
                if guess[x, y] > max_output:
                    max_output = guess[x, y]
                    max_x = x
                    max_y = y
        return max_x, max_y

    def mutate(self, rate):
        """
        mutates neural net inplace
        :param rate: probability of mutation
        :type rate: int
        """
        
        self.brain.mutate(rate)

    @staticmethod
    def update_fitness(winner, loser, tie=False, k=32):
        """
        Updates the fitness of two neural net players after a game
        :param winner: the winning player
        :type winner: NNPlayer
        :param loser: the losing player
        :type loser: NNPlayer
        :param tie: if the game ended in a tie
        :type tie: bool
        :param k: how imortant the game was
        :type k: int
        """

        transformed_winner_fitness = np.power(10, winner.elo / 400.0)
        transformed_loser_fitness = np.power(10, loser.elo / 400.0)

        expected_winner = transformed_winner_fitness / (transformed_winner_fitness + transformed_loser_fitness)
        expected_loser = transformed_loser_fitness / (transformed_winner_fitness + transformed_loser_fitness)

        winner.elo += k * ((1 - (0.5 * tie)) - expected_winner)
        loser.elo += k * ((0.5 * tie) - expected_loser)


if __name__ == '__main__':
    bot = NNPlayer()
    print(bot.play(((1,2,3), (4,5,6),(7,8,9))))
