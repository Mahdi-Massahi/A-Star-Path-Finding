import Game
import math
import time
import UI.Decorator as UI


class AStar:
    def __init__(self, game: Game):
        self.game = game

        self.open_set = []
        self.closed_set = []
        self.shortest_path = []

    def solve(self):

        is_done = False
        did_win = False

        while not(is_done or did_win):

            # get the current position
            current_position = self.game.get_current_position()

            # find neighbors of current
            neighbors = self.game.get_neighbors_position()

            # exclude those which exist in closed_set
            for neighbor in neighbors:
                if neighbor in self.closed_set:
                    neighbors.remove(neighbor)

            # exclude those which exist in open_set TODO is it right?!
            for neighbor in neighbors:
                if neighbor in self.open_set:
                    neighbors.remove(neighbor)

            # only new neighbors
            new_neighbors = neighbors.copy()

            # if any neighbor is left, add it to open_set
            if len(new_neighbors) > 0:
                self.open_set = self.add_neighbors(old=self.open_set,
                                                   members=new_neighbors)
                # set parents for new_neighbors
                self.game.set_parent_node(
                    parent_position=current_position,
                    children_position=new_neighbors
                )

            # calculate f score for neighbors
            self.calculate_f_scores(new_neighbors)

            # once again remove nodes which are closed from open_set TODO don't know why some exist for now
            for closed_node in self.closed_set:
                if closed_node in self.open_set:
                    self.open_set.remove(closed_node)

            # move to lowest f score node and get the new position
            current_position = self.move_to_lowest_f_score(self.open_set)

            # drop current_position from open_list
            if len(self.open_set) > 0:
                self.open_set.remove(current_position)

            # add current_position to closed_set
            if current_position not in self.closed_set:
                self.closed_set.append(current_position)

            # check if won
            did_win = self.game.do_win()
            if did_win:
                print("Won!")

                # generate shortest path using close_set
                self.shortest_path = self.get_shortest_path()

            # check if there is no path to goal
            if len(self.open_set) == 0 and not did_win:
                print("No path found.")
                is_done = True

            # search will continue

            # plot the game
            self.game.grid.plot()
            print("Phase done")


    @staticmethod
    def add_neighbors(old: [tuple], members: [tuple]):
        new = old.copy()
        for member in members:
            if member not in old:
                new.append(member)
        return new

    def get_relative_g_scores(self, neighbors_position: [tuple], current_position: tuple):
        relative_g_scores = []
        if len(neighbors_position) > 0:
            for neighbor_position in neighbors_position:
                g_score = self.get_g_score(neighbor_position)
                # TODO change fallowing method if diagonal moves are applied
                relative_g_scores.append(g_score + 1)
        return relative_g_scores

    def get_g_score(self, position: tuple):
        start = self.game.grid.start_position
        g_score = abs(start[0] - position[0]) + abs(start[1] - position[1])
        return g_score

    def get_g_scores(self, positions: [tuple]):
        g_scores = []
        if len(positions) > 0:
            for position in positions:
                g_scores.append(self.get_g_score(position))
        return g_scores

    # TODO change the method for calculation
    def calculate_and_get_g_score(self, position: tuple):
        g_score = self.get_g_score(position)
        self.game.grid.grid[position[0]][position[1]].gScore = g_score
        return g_score

    def calculate_and_get_h_score(self, position: tuple):
        goal = self.game.grid.goal_position
        h_score = abs(goal[0] - position[0]) + abs(goal[1] - position[1])
        self.game.grid.grid[position[0]][position[1]].hScore = h_score
        return h_score

    def calculate_f_scores(self, nodes_position: [tuple]):
        if len(nodes_position) > 0:
            for node_position in nodes_position:
                x = node_position[0]
                y = node_position[1]
                f_score = self.calculate_and_get_g_score((x, y)) + \
                          self.calculate_and_get_h_score((x, y))
                self.game.grid.grid[x][y].fScore = f_score

    def get_f_scores(self, nodes_position: [tuple]):
        f_scores = []
        if len(nodes_position) > 0:
            for node_position in nodes_position:
                x = node_position[0]
                y = node_position[1]
                f_scores.append(self.game.grid.grid[x][y].fScore)
        return f_scores

    def move_to_lowest_f_score(self, nodes_position: [tuple]):
        if len(nodes_position) > 0:
            f_scores = self.get_f_scores(nodes_position)
            index_min_f_scores = f_scores.index(min(reversed(f_scores)))  # f_scores.index(min(reversed(f_scores)))
            min_f_score_node_position = nodes_position[::-1][index_min_f_scores]  # nodes_position[::-1][index_min_f_scores]
            self.game.change_current(min_f_score_node_position)
            return min_f_score_node_position

    def get_shortest_path(self):
        parents = []
        start_position = self.game.grid.start_position
        current_position = self.game.get_current_position()
        while start_position != current_position:
            current_parent_position = self.game.grid.grid[current_position[0]][current_position[1]].parent
            parents.append(current_parent_position)
            self.game.grid.grid[current_parent_position[0]][current_parent_position[1]].Type = UI.CellType.Path
            current_position = current_parent_position

        return parents