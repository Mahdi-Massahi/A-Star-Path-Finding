import UI.Decorator as UI


class Game:
    def __init__(self, width: int, height: int, alpha=0):
        self.grid = UI.Grid(
            height=height,
            width=width,
            alpha=alpha
        )
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
                if cell.Type == UI.CellType.Current:
                    return cell.x, cell.y
        for row in plat:
            for cell in row:
                if cell.Type == UI.CellType.Start:
                    return cell.x, cell.y

    def is_win(self):
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
                if cell.Type != UI.CellType.Blocked:
                    open_set.append(cell)
        return open_set

    def change_current(self, new_current):
        current = self.get_current_position()
        self.grid.grid[current[0]][current[1]].Type = UI.CellType.Visited
        self.grid.grid[new_current[0]][new_current[1]].Type = UI.CellType.Current

    def get_neighbors(self):
        neighbors = []
        current = self.get_current_position()
        if current is None:
            return []
        x, y = current

        if x-1 > 0:
            if self.grid.grid[x-1][y].Type != UI.CellType.Blocked:
                neighbors.append(self.grid.grid[x-1][y])
        if y-1 > 0:
            if self.grid.grid[x][y-1].Type != UI.CellType.Blocked:
                neighbors.append(self.grid.grid[x][y-1])
        if x+1 < self.grid.height:
            if self.grid.grid[x+1][y].Type != UI.CellType.Blocked:
                neighbors.append(self.grid.grid[x+1][y])
        if y+1 < self.grid.width:
            if self.grid.grid[x][y+1].Type != UI.CellType.Blocked:
                neighbors.append(self.grid.grid[x][y+1])

        return neighbors


