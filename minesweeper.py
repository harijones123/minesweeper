import random as rd 

def get_neighbours(square):
    x,y = square
    neighbours = [(x-1,y+1),(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]
    neighbours = [n for n in neighbours if (0<=n[0]<=cols) and (0<=n[1]<=rows)]
    return neighbours

class game:
    def __init__(self, rows, cols, n_mines):
        self.rows = rows
        self.cols = cols
        self.n_mines = n_mines
        self.board = [[0 for i in range(0,rows)] for j in range(0,cols)]
        self.board_coords = [(x,y) for x in range(0,cols) for y in range(0,rows)]
        self.board_revealed = [[False for i in range(0,rows)] for j in range(0,cols)]
    def make_first_move(self,selection=None):
        if selection is None:
            selection = rd.choice(self.board_coords)
        self.board = generate_board(rows,cols,n_mines,first_move=selection) 
    def generate_board(self,first_move=None) :
        #generate potential mines
        if first_move is not None:
            #make sure first move is a 0
            board_coords_temp = self.board_coords.remove(first_move)
            first_move_nbrs = get_neighbours(first_move)
            board_coords_temp = [c for c in board_coords_temp if c not in first_move_nbrs]
        #get random sample of potential mines
        mine_coords = rd.sample(board_coords_temp,n_mines)
        self.mine_coords = mine_coords
        #fill in numbers around mines
        for mine in mine_coords:
            x,y = mine
            board[x][y] = 9
            neighbours = get_neighbours(mine)
            for n in neighbours:
                if n not in mine_coords:
                    board[n[0]][n[1]] = board[n[0]][n[1]] + 1
        return board
    def select_cell(self,selection):
        x,y = selection
        selection_value = self.board[x][y]
        if selection_value == 9:
            #selected mine, game over
            print("GAME OVER")
            exit(-1)
        else:
            reveal_cell(selection)
    def reveal_cell(self,selection):
        x,y = selection
        selection_value = self.board[x][y]
        if selection_value==0:
            selection_nbrs = get_neighbours(selection)
            for n in selection_nbrs:
                reveal_cell(n)
        self.board_revealed[x][y] = True

        

#initialise game
currentGame = game(9,9,10)
#first move (generate board once first move is made)
currentGame.make_first_move()


first_move = rd.





print(board)

