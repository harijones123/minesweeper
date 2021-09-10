import random
import numpy as np
import time

def get_neighbours(square,cols,rows):
    x,y = square
    neighbours = [(x-1,y+1),(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]
    neighbours = [n for n in neighbours if ((0<=n[0]<cols) and (0<=n[1]<rows))]
    return neighbours
def user_input():
    type,x,y = input("Select cell:").split()
    cell = tuple([int(x),int(y)])
    return type.upper(),cell
    
class Game:
    def __init__(self, rows, cols, n_mines):
        self.rows = rows
        self.cols = cols
        self.n_mines = n_mines
        self.board = [[0 for i in range(0,rows)] for j in range(0,cols)]
        self.board_coords = [(x,y) for x in range(0,cols) for y in range(0,rows)]
        self.revealed_coords = set([])
        self.gameState = "playing"
    def make_first_move(self,selection=None):
        if selection is None:
            selection = random.choice(self.board_coords)
        self.generate_board(first_move=selection) 
        self.select_cell(selection)
    def generate_board(self,first_move=None) :
        #generate potential mines
        if first_move is not None:
            #make sure first move is a 0
            board_coords_temp = self.board_coords
            board_coords_temp.remove(first_move)
            first_move_nbrs = get_neighbours(first_move,self.cols,self.rows)
            board_coords_temp = [c for c in board_coords_temp if c not in first_move_nbrs]
        #get random sample of potential mines
        mine_coords = random.sample(board_coords_temp,self.n_mines)
        self.mine_coords = mine_coords
        #fill in numbers around mines
        for mine in mine_coords:
            x,y = mine
            self.board[x][y] = 9
            neighbours = get_neighbours(mine,self.cols,self.rows)
            for n in neighbours:
                if n not in mine_coords:
                    self.board[n[0]][n[1]] = self.board[n[0]][n[1]] + 1
    def select_cell(self,selection):
        x,y = selection
        selection_value = self.board[x][y]
        if selection_value == 9:
            #selected mine, game over
            self.gameState = "gameover"
            self.board[x][y] = 11
        else:
            self.reveal_cell(selection)
    def flag_cell(self,cell):
        x,y = cell
        self.board[x][y] = 10
        self.revealed_coords.add((x,y))
    def reveal_cell(self,selection):
        x,y = selection
        if (x,y) not in self.revealed_coords:
            self.revealed_coords.add((x,y))
            selection_value = self.board[x][y]
            if selection_value==0:
                selection_nbrs = get_neighbours(selection,self.cols,self.rows)
                for n in selection_nbrs:
                    self.reveal_cell(n)
    def show_board(self,t=0):
        if self.gameState == "gameover":
            for mine in self.mine_coords:
                x,y = mine
                self.revealed_coords.add((x,y))
        board_disp = [[" " for i in range(0,self.rows)] for j in range(0,self.cols)]
        for coord in self.revealed_coords:
            x,y = coord
            board_disp[x][y] = self.board[x][y]

        board_disp = np.array(board_disp).astype("str")
        board_disp[board_disp=="9"] = "M"
        board_disp[board_disp=="10"] = "F"
        board_disp[board_disp=="11"] = "B"
        print(board_disp)
        time.sleep(t)
    def play_turn(self):
        move,cell = user_input()
        if move == "F":
            self.flag_cell(cell)
        elif move == "R":
            self.select_cell(cell)
        self.show_board()
    def play_game(self):
        move,cell = user_input()
        if move == "F":
            print("Currently don't support Flag as first move")
            self.gameState = "gameover"
        elif move == "R":
            self.make_first_move(cell)
            self.show_board()
        while self.gameState == "playing":
            self.play_turn()
            self.win_condition()
            if self.gameState == "winner":    
                print("Winner winner chicken dinner")
            if self.gameState == "gameover":    
                print("Game Over")
    def win_condition(self):
        if len(self.revealed_coords)==self.cols*self.rows:
            self.gameState = "winner"