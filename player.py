from board import Board, IllegalMoveError, GameOverError
class IllegalPlayerNumber(Exception):
    pass

class BasePlayer(object):
    def __init__(self, player_number):
        if player_number not in (1, 2):
            raise IllegalPlayerNumber
        self.player_number = player_number
        
    def take_turn(board):
        pass
        
        
class HumanPlayer(BasePlayer):
    def take_turn(self, board):
        print('Player {}\'s turn'.format(self.player_number))
        board.display()
        print()
        while True:
            move = input('Where woud you like to go? [x,y] >>> ')
            move = move.replace(" ", "").replace('[', '').replace(']', '')
            try:
                x, y = move.split(',')
                pos = int(x), int(y)
                result = board.play(pos, self.player_number)
                break
            except ValueError:
                print('Please enter two numbers seperated by a comma')
            except IllegalMoveError:
                print('That move is not legal')
            except GameOverError:
                print('The game is over')
                break
        print('\n\n')
        if result:
            print('Player {} Wins!!'.format(self.player_number))
            board.display()
            return True
        return False

if __name__ == '__main__':
    current_player = HumanPlayer(1)
    next_player = HumanPlayer(2)
    board = Board()
    while True:
        if current_player.take_turn(board):
            break
        else:
            current_player, next_player = next_player, current_player
        

        
        
        
