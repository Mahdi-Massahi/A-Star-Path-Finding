from Game import Game
from Algo import AStar
import random

ch = ""

while ch == "":
    width = random.randrange(5, 20)
    height = random.randrange(5, 20)
    game = Game(width=width, height=height, alpha=0.5)

    algo = AStar(game=game)
    algo.solve()

    ch = input("Repeat? (Yes: Enter)")
