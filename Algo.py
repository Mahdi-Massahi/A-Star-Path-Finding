import Game
import math
import time
import UI.Decorator as UI


class AStar:
    def __init__(self, game: Game):
        self.game = game

        """openSet := {start}"""
        self.open_set = [] # self.game.get_open_set()

        """cameFrom := an empty map"""
        self.came_from = []

    def solve(self):
        self.initialize_g_score()
        self.initialize_f_score()

        # remove here
        neighbors = self.game.get_neighbors()
        self.open_set = neighbors
        # to here

        is_done = False

        """while openSet is not empty"""
        while len(self.open_set) > 0 and not is_done:

            """current := the node in openSet having the lowest fScore[] value"""
            f_scores = self.get_f_scores()
            index_min_f_score = f_scores.index(min(f_scores))
            min_f_score_cell = self.open_set[index_min_f_score]
            new_current = min_f_score_cell.x, min_f_score_cell.y
            self.game.change_current(new_current)

            """if current = goal"""
            if self.game.is_win():
                """return reconstruct_path(cameFrom, current)"""
                self.reconstruct_path()
                is_done = True

            """openSet.Remove(current)"""
            self.open_set.pop(index_min_f_score)

            """for each neighbor of current"""
            neighbors = self.game.get_neighbors()
            for neighbor in neighbors:

                """tentative_gScore := gScore[current] + d(current, neighbor)"""
                current = self.game.get_current_position()
                tentative_gScore = self.get_g_score(current) + 0

                # TODO maybe i should calculate g-score for neighbors first
                """if tentative_gScore < gScore[neighbor]"""
                g_score = self.get_g_score((neighbor.x, neighbor.y))
                if tentative_gScore < g_score:

                    """cameFrom[neighbor] := current"""
                    self.came_from.append((neighbor.x, neighbor.y))

                    """gScore[neighbor] := tentative_gScore"""
                    self.game.grid.grid[neighbor.x][neighbor.y].gScore = tentative_gScore

                    """fScore[neighbor] := gScore[neighbor] + h(neighbor)"""
                    self.game.grid.grid[neighbor.x][neighbor.y].fScore = \
                        tentative_gScore + self.heuristic((neighbor.x, neighbor.y))

                    """if neighbor not in openSet"""
                    if neighbor not in self.open_set:

                        """openSet.add(neighbor)"""
                        self.open_set.append(neighbor)

            self.game.grid.plot()

        """return failure"""
        # TODO SOLOV THIS
        if not is_done:
            print("There is no path to end.")

    def initialize_g_score(self,):
        """
        gScore := map with default value of Infinity
        gScore[start] := 0
        """
        for row in self.game.grid.grid:
            for cell in row:
                cell.gScore = 1e10
        self.game.grid.grid[0][0].gScore = 0

    def initialize_f_score(self):
        """
        fScore := map with default value of Infinity
        fScore[start] := h(start)
        """
        for row in self.game.grid.grid:
            for cell in row:
                cell.fScore = 1e10
        self.game.grid.grid[0][0].fScore = self.heuristic(position=(0, 0))

    def heuristic(self, position):
        goal = self.game.grid.goal_position
        return math.sqrt(pow(goal[0]-position[0], 2) + pow(goal[1]-position[1], 2))

    def get_f_scores(self):
        f_scores = []
        for cell in self.open_set:
            f_scores.append(cell.fScore)
        return f_scores

    def get_g_score(self, position):
        start = self.game.grid.start_position
        return math.sqrt(abs(start[0] - position[0]) + abs(start[1] - position[1]))

    def reconstruct_path(self):
        total_path = []

        """total_path := {current}"""
        current = self.game.get_current_position()
        total_path.append(current)

        """while current in cameFrom.Keys:"""
        for came_from in self.came_from:
            total_path.append(came_from)

        for cell in total_path:
            self.game.grid.grid[cell[0]][cell[1]].Type = UI.CellType.Path

        print("Best path is found.")




