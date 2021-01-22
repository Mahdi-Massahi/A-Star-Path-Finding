from Game import Game
from Algo import AStar

game = Game(width=15, height=15, alpha=0.4)

algo = AStar(game=game)

algo.solve()

print(algo.game)

input("Exit?")

