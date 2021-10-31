from game import Game
from player_v3 import Player
import matplotlib.pyplot as plt
import numpy as np

N = 1000
n_mines = list(range(5,26,5))
NN = list(range(6,17,2))

winrateses = []
for nn in NN:
    winrates = []
    for mines in n_mines:
        results = []
        if nn*nn-9 > mines:
            for i in range(N):
                currentGame = Game(nn,nn,mines)
                currentPlayer = Player(currentGame)
                result = currentPlayer.play_game_eval()
                results.append(result)
            winrate = results.count("winner")/N
        else:
            winrate = np.nan
        winrates.append(winrate)
        print("NN: {nn}, N_mines: {n_mines}, winrate: {winrate}".format(nn=nn,n_mines=mines,winrate=winrate))
    winrateses.append(winrates)
        
for winrates in winrateses:
    plt.plot(n_mines,winrates)
plt.title("Win-rate performance evaluation, v3")
plt.xlabel("Number of mines")
plt.ylabel("Win rate")
plt.legend(["{nn}x{nn}".format(nn=x) for x in NN],title="Board size")
plt.show()
