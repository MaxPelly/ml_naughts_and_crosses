import re


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
