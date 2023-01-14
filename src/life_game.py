from random import randint

from cell import Cell

class LifeGame:
    def __init__(self, width: int=10, height: int=10) -> None:
        self._width = width 
        self._height = height 
        self._is_ended = False 
        self._board = [ [Cell.DEAD]*height for _ in range(width) ]
    

    def get_board(self):
        board = []
        for row in self._board:
            (row_copy:=[]).extend(row)
            board.append(row_copy)
        return board
    def set_random_cell_alive(self, total=50):
        while total != 0 :
            x=randint(0, self._width-1)
            y=randint(0, self._height-1)
            self._board[x][y]=Cell.LIFE
            total-=1

    def next_generation(self):
        next_board = [ [Cell.DEAD]*self._height for _ in range(self._width) ]
        self._is_ended = True
        for i in range(self._width):
            for j in range(self._height):
                next_board[i][j]=self._get_next_state(i,j)
                if next_board[i][j] != self._board[i][j]:
                    self._is_ended=False
        
        self._board = next_board

    def insert_configuration_in(self, x: int, y: int, cells: list[list[Cell]]):
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                if self._verify_pos(x+i,y+j):
                    self._board[x+i][y+j] = cells[i][j]


    @property
    def is_game_ended(self): return self._is_ended

    def _verify_pos(self, x: int, y: int):
        return x >= 0 and x < self._width and\
               y >= 0 and y < self._height

    _helper_x = [1,0,-1,0,1,1,-1,-1]
    _helper_y = [0,1,0,-1,-1,1,1,-1]
    def _get_next_state(self,x:int,y:int):
        #alive = 1 if self._board[x][y] == Cell.LIFE else 0
        alive=0
        for k in range(len(LifeGame._helper_x)):
            xx=x + LifeGame._helper_x[k]
            yy=y + LifeGame._helper_y[k]
            if self._verify_pos(xx,yy) and self._board[xx][yy] == Cell.LIFE :
                alive+=1

        if self._board[x][y] == Cell.LIFE and 2 <= alive <= 3:
            return Cell.LIFE
        elif self._board[x][y] == Cell.DEAD and alive == 3:
            return Cell.LIFE
        return Cell.DEAD


