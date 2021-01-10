from Game import Game
from Algo import AStar

game = Game(width=20, height=20, alpha=0.2)

algo = AStar(game=game)

algo.solve()

print(algo.game)

input("Exit?")

