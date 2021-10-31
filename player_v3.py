#changes limited to find_mines()
import random
import numpy as np
import time
from game import Game

def get_neighbours(square,cols,rows):
    x,y = square
    neighbours = [(x-1,y+1),(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]
    neighbours = [n for n in neighbours if ((0<=n[0]<cols) and (0<=n[1]<rows))]
    return neighbours

class Player:
    def __init__(self,game):
        self.game = game
        self.active_cells = set([])
        self.flagged_coords = set([])
    def make_first_move(self):
        self.game.make_first_move()
        self.refresh_active_cells()
    def refresh_active_cells(self):
        for coord in self.game.revealed_coords:
            nbrs = get_neighbours(coord,self.game.cols,self.game.rows)
            if len(self.game.revealed_coords.intersection(nbrs))!=len(nbrs):
                self.active_cells.add(coord)
            elif coord in self.active_cells:
                self.active_cells.remove(coord)
    def find_mines(self,coord,nbrs):
        x,y = coord
        unrevealed_nbrs = set(nbrs) - self.game.revealed_coords
        flagged_nbrs = self.flagged_coords.intersection(nbrs)
        if len(unrevealed_nbrs)+len(flagged_nbrs) == self.game.board[x][y]:
            for cell in unrevealed_nbrs:
                self.game.flag_cell(cell)
                self.flagged_coords.add(cell)
        elif 1<self.game.board[x][y]<=8:
            flagged_nbrs = self.flagged_coords.intersection(nbrs)
            self.find_mines_2(coord,nbrs,unrevealed_nbrs,flagged_nbrs)
        self.game.win_condition()
    def find_mines_2(self,coord,nbrs,unrevealed_nbrs,flagged_nbrs):
        "if cell in question is a 2,3,4,+, look out for any 1s that are touching it, and use overlap technique to identify mines"
        x,y = coord
        active_neighbours = self.active_cells.intersection(nbrs)
        one_neighbours = {x for x in active_neighbours if self.game.board[x[0]][x[1]]==1}
        #one_neighbours = filter(lambda x: self.game.board[x[0]][x[1]]==1, active_neighbours)
        if len(one_neighbours)!=0:
            for one_nbr in one_neighbours:
                nbrs1 = get_neighbours(one_nbr,self.game.cols,self.game.rows)
                unrevealed_nbrs1 = set(nbrs1) - self.game.revealed_coords
                overlap = unrevealed_nbrs.intersection(unrevealed_nbrs1)
                unrevealed_left = unrevealed_nbrs - overlap
                if (len(overlap)>1) and (len(unrevealed_left)==self.game.board[x][y]-1-len(flagged_nbrs)):
                    for cell in unrevealed_left:
                        self.game.flag_cell(cell)
                        self.flagged_coords.add(cell)

    def find_safe(self,coord,nbrs):
        x,y = coord 
        flagged_nbrs = self.flagged_coords.intersection(nbrs)
        if len(flagged_nbrs) >= self.game.board[x][y]:
            for cell in set(nbrs) - self.game.revealed_coords - flagged_nbrs:
                self.game.select_cell(cell)
        self.game.win_condition()
    def play_turn(self):
        for coord in self.active_cells:
            nbrs = get_neighbours(coord,self.game.cols,self.game.rows)
            if self.game.gameState == "playing":
                self.find_mines(coord,nbrs)
            if self.game.gameState == "playing":
                self.find_safe(coord,nbrs)
        self.refresh_active_cells()
    def make_guess(self):
        #get all cells that are potential to be selected
        neighbours = set([])
        for active_cell in self.active_cells:
            neighbours.update(get_neighbours(active_cell,self.game.cols,self.game.rows))
        potential_cells = neighbours - self.game.revealed_coords

        if len(potential_cells)>0:
            #loop through these and assign cumulative probabilities for each one being a mine
            prob_guess = dict.fromkeys(potential_cells, 0)
            for active_cell in self.active_cells:
                x,y = active_cell
                if self.game.board[x][y]!=10:
                    neighbours = get_neighbours(active_cell,self.game.cols,self.game.rows)
                    potential_nbrs = set(neighbours) - self.game.revealed_coords
                    for nbr in potential_nbrs:
                        prob_guess[nbr] = prob_guess[nbr] + self.game.board[x][y]/len(potential_nbrs)
            
            #select random value from the least likely to be mines
            least_likely = [k for k,v in prob_guess.items() if v == prob_guess[min(prob_guess, key=prob_guess.get)]]
            self.game.select_cell(random.choice(list(least_likely)))
        
    def play_game(self,t=0):
        self.game.show_board(t)
        self.make_first_move()
        self.game.show_board(t)
        revealed_coords_prev = set([])
        while self.game.gameState == "playing":
            print(self.game.gameState)
            self.play_turn()
            if self.game.revealed_coords == set(revealed_coords_prev):
                self.make_guess()
            revealed_coords_prev = list(self.game.revealed_coords)
            self.game.show_board(t)
        print(self.game.gameState)
    def play_game_eval(self):
        self.make_first_move()
        revealed_coords_prev = set([])
        while self.game.gameState == "playing":
            self.play_turn()
            if self.game.revealed_coords == set(revealed_coords_prev):
                self.make_guess()
            revealed_coords_prev = list(self.game.revealed_coords)
        return self.game.gameState 

currentGame = Game(8,8,10)
currentPlayer = Player(currentGame)
currentPlayer.play_game()