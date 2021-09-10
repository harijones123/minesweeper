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
        self.game.win_condition()
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
        neighbours = set([])
        for active_cell in self.active_cells:
            neighbours.update(get_neighbours(active_cell,self.game.cols,self.game.rows))
        potential_cells = neighbours - self.game.revealed_coords
        self.game.select_cell(random.choice(list(potential_cells)))
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

#initialise game
currentGame = Game(8,8,10)
currentPlayer = Player(currentGame)
currentPlayer.play_game(2)
