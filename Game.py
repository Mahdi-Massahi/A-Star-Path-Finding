import UI.Decorator as UI


class Game:
    def __init__(self, width: int, height: int, alpha=0):
        self.grid = UI.Grid(height=height, width=width, alpha=alpha)
        self.path = []

    def set_start(self, x: int, y: int):
        self.grid.set_start(x, y)

    def set_goal(self, x: int, y: int):
        self.grid.set_goal(x, y)

    def show(self):
        self.grid.plot()

    def get_current_position(self):
        plat = self.grid.grid
        for row in plat:
            for cell in row:
                if cell.type == UI.CellType.Current:
                    return cell.x, cell.y
        for row in plat:
            for cell in row:
                if cell.type == UI.CellType.Start:
                    return cell.x, cell.y

    def do_win(self):
        current = self.get_current_position()
        goal = self.grid.goal_position
        if current == goal:
            return True
        return False

    def get_open_set(self):
        open_set = []
        plat = self.grid.grid
        for row in plat:
            for cell in row:
                if cell.type != UI.CellType.Blocked:
                    open_set.append(cell)
        return open_set

    def change_current(self, new_current):
        current = self.get_current_position()
        self.grid.grid[current[0]][current[1]].type = UI.CellType.Highlighted
        self.grid.grid[new_current[0]][
            new_current[1]
        ].type = UI.CellType.Current

    def update_visible_nodes(self, open_set: [tuple]):
        for node in open_set:
            self.grid.grid[node[0]][node[1]].type = UI.CellType.Visited

    def get_neighbors_position(self):
        neighbors = []
        current = self.get_current_position()
        if current is None:
            return []
        x, y = current

        # Orthogonal
        if x - 1 >= 0:
            if self.grid.grid[x - 1][y].type != UI.CellType.Blocked:
                neighbors.append(
                    (self.grid.grid[x - 1][y].x, self.grid.grid[x - 1][y].y)
                )
        if y - 1 >= 0:
            if self.grid.grid[x][y - 1].type != UI.CellType.Blocked:
                neighbors.append(
                    (self.grid.grid[x][y - 1].x, self.grid.grid[x][y - 1].y)
                )
        if x + 1 < self.grid.height:
            if self.grid.grid[x + 1][y].type != UI.CellType.Blocked:
                neighbors.append(
                    (self.grid.grid[x + 1][y].x, self.grid.grid[x + 1][y].y)
                )
        if y + 1 < self.grid.width:
            if self.grid.grid[x][y + 1].type != UI.CellType.Blocked:
                neighbors.append(
                    (self.grid.grid[x][y + 1].x, self.grid.grid[x][y + 1].y)
                )

        # Diagonal
        if y + 1 < self.grid.width and x + 1 < self.grid.height:
            if self.grid.grid[x + 1][y + 1].type != UI.CellType.Blocked:
                neighbors.append(
                    (
                        self.grid.grid[x + 1][y + 1].x,
                        self.grid.grid[x + 1][y + 1].y,
                    )
                )
        if y + 1 < self.grid.width and x - 1 >= 0:
            if self.grid.grid[x - 1][y + 1].type != UI.CellType.Blocked:
                neighbors.append(
                    (
                        self.grid.grid[x - 1][y + 1].x,
                        self.grid.grid[x - 1][y + 1].y,
                    )
                )
        if y - 1 >= 0 and x + 1 < self.grid.height:
            if self.grid.grid[x + 1][y - 1].type != UI.CellType.Blocked:
                neighbors.append(
                    (
                        self.grid.grid[x + 1][y - 1].x,
                        self.grid.grid[x + 1][y - 1].y,
                    )
                )
        if y - 1 >= 0 and x - 1 >= 0:
            if self.grid.grid[x - 1][y - 1].type != UI.CellType.Blocked:
                neighbors.append(
                    (
                        self.grid.grid[x - 1][y - 1].x,
                        self.grid.grid[x - 1][y - 1].y,
                    )
                )

        return neighbors

    def set_parent_node(
        self, parent_position: tuple, children_position: [tuple]
    ):
        if len(children_position) > 0:
            for child_position in children_position:
                x = child_position[0]
                y = child_position[1]
                self.grid.grid[x][y].parent = parent_position
