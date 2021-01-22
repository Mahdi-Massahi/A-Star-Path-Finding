from Game import Game
from Algo import AStar
import random

ch = "Yes"

while ch[0] in ['Y', 'y']:
    width = random.randrange(5, 20)
    height = random.randrange(5, 20)
    game = Game(width=width, height=height, alpha=0.5)

    algo = AStar(game=game)
    algo.solve()

    print(algo.game)

    ch = input("Repeat? (Yes/No)")



