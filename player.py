import re
from nn import Neural_Net
import numpy as np


class BasePlayer(object):
    def __init__(self):
        pass
        
    def take_turn(self, state):
        pass
        
        
class HumanPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.move_checker = re.compile('[0-2],[0-2]')

    def play(self, state, player_number):
        print('Player {}\'s turn'.format(player_number))
        self.display(state)
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

    @staticmethod
    def display(state):
        for y in range(3):
            out_str = '|'
            for x in range(3):
                out_str += '{}|'.format(state[x][y])
            print(out_str)
        print()


class NNPlayer(BasePlayer):
    def __init__(self, net_shape = (9, 18, 9, 9)):
        super().__init__()
        self.brain = Neural_Net(net_shape)

    def play(self, state, *args, **kwargs):
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


if __name__ == '__main__':
    bot = NNPlayer()
    print(bot.play(((1,2,3), (4,5,6),(7,8,9))))
