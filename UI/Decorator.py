from random import randrange
import subprocess
import platform


class Grid:
    def __init__(self, width: int, height: int, alpha=0.0):
        self.grid = [
            [Cell(i, j) for j in range(width)] for i in range(height)
        ]
        self.width = width
        self.height = height
        for i in range(self.width):
            for j in range(self.height):
                if randrange(0, 100) < alpha * 100:
                    # if (
                    #         # img 1
                    #         # (j, i) == (2, 2) or
                    #         # (j, i) == (3, 2) or
                    #         # (j, i) == (2, 3)
                    #
                    #         # img 2
                    #         (j, i) == (0, 2) or
                    #         (j, i) == (2, 1) or
                    #         (j, i) == (2, 3) or
                    #         (j, i) == (2, 2)
                    # ):
                    self.grid[j][i].type = CellType.Blocked
        self.start_position = (0, 0)
        self.goal_position = (self.height - 1, self.width - 1)
        self.grid[0][0].type = CellType.Start
        self.grid[self.height - 1][self.width - 1].type = CellType.Goal

    def set_start(self, x, y):
        self.grid[y][x].type = CellType.Start
        self.start_position = (x, y)

    def set_goal(self, x, y):
        self.grid[y][x].type = CellType.Goal
        self.goal_position = (x, y)

    def plot(self):
        if platform.system() == "Windows":
            subprocess.Popen("cls", shell=True).communicate()
        else:  # Linux and Mac
            print("\033c", end="")
        print("     ", end="")
        for i in range(self.width):
            print("{0:>2} ".format(i), end="")
        print()
        print("   ╔═", end="")
        for i in range(self.width):
            if i != self.width - 1:
                print("══╤", end="")
        print("═══╗")
        j = 0
        for row in self.grid:
            print("{0:>2} ║ ".format(j), end="")
            i = 0
            for cell in row:
                print(f"{self.grid[j][i].type}", end="")
                if i != self.width - 1:
                    print(" ", end="")
                i += 1
            print(" ║")
            j += 1
        print("   ╚═", end="")
        for i in range(self.width):
            if i != self.width - 1:
                print("══╧", end="")
        print("═══╝")


class CellType:
    Blocked = "██"
    Normal = "  "
    Visited = "░░"
    Highlighted = "▒▒"
    Path = "**"
    Current = "CU"
    Start = "ST"
    Goal = "GO"


class Cell:
    def __init__(self, x, y, kind=CellType.Normal):
        self.x = x
        self.y = y
        self.type = kind
        self.parent = None
        self.fScore = None
        self.gScore = None
        self.hScore = None
