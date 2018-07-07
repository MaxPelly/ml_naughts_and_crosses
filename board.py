class IllegalMoveError(Exception):
    pass
    
class GameOverError(Exception):
    pass

class Board (object):
    
    '''
    creates the board object with an array of 0s in self.state for the board
    0 is an empty square, 1 is a cross and 2 is a naught (players 1 and 2)
    '''
    def __init__(self):
        self.state = [[0 for _ in range(3)] for __ in range(3)]
        self.won = False
        self.winner = 0
        
    def get(self, pos):
        return self.state[pos[0]][pos[1]]
        
    def set(self, pos, val):
        self.state[pos[0]][pos[1]] = val
        
    '''
    plays a turn for player at pos.
    player should be a number 1 or 2
    pos should be an array or tuple of ints (x,y) between 0 and 2
    returns true if the move can be made, otherwise false
    '''  
    def play(self, pos, player):
        if player not in (1,2) or pos[0] not in (0,1,2) or pos[1] not in (0,1,2) or self.get(pos) != 0:
            raise IllegalMoveError()
        if self.won:
            raise GameOverError()
        self.set(pos, player)
        return self._test_for_win(pos, player)
    
    def _test_for_win(self, pos, player):
        x = pos[0]
        y = pos[1]
        to_check = {0: (1, 2), 1: (-1, 1), 2: (-1, -2)}
        check_x = to_check[x]
        check_y = to_check[y]
        self.won =  (player == self.get((x + check_x[0], y)) and player == self.get((x + check_x[1], y))) or (player == self.get((x, y + check_y[0])) and player == self.get((x, y + check_y[1])))
        self.winner = self.won * player
        return self.won
        
    def display(self):
        for y in range(3):
            str = '|'
            for x in range(3):
                str += '{}|'.format(self.state[x][y])
            print(str)
        print()
                
         
                

