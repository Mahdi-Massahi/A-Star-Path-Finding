from Game import Game
from Algo import AStar

game = Game(width=5, height=5, alpha=0.4)

algo = AStar(game=game)

algo.solve()

print(algo.game)

input("Exit?")

