import time
import random
from cell import Cell

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        """Initialize the maze with an optional Window reference for testing."""
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win  # Optional window for graphical rendering

        if seed is not None:
            random.seed(seed)  # Allows for repeatable mazes

        self._cells = []
        self._create_cells()

        if self._num_cols > 0 and self._num_rows > 0:
            self._break_entrance_and_exit()
            self._break_walls_r(0, 0)  # Generate the maze using DFS
            self._reset_cells_visited()

        self._reset_cells_visited()  # Ensure visited property is reset before solving

    def _create_cells(self):
        """Creates a grid of cells before drawing."""
        if self._num_cols == 0 or self._num_rows == 0:
            return

        self._cells = []  # Reset cell list

        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size_x
                y1 = self._y1 + j * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                column.append(Cell(x1, y1, x2, y2, self._win))
            self._cells.append(column)

    def _draw_cell(self, i, j):
        """Draws a single cell at position (i, j) with animation, if applicable."""
        if self._win:
            self._cells[i][j].draw()
            self._animate()

    def _animate(self):
        """Redraws the window and sleeps for a short time to create an animation effect."""
        if self._win:
            self._win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        """Breaks the entrance (top-left cell) and exit (bottom-right cell)."""
        if not self._cells:
            return

        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        """Recursively breaks walls using Depth-First Search (DFS)."""
        cell = self._cells[i][j]
        cell.visited = True  # Mark current cell as visited

        # Store possible directions: (dx, dy, direction)
        directions = []
        if i > 0 and not self._cells[i - 1][j].visited:  # Left
            directions.append((-1, 0, "left"))
        if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:  # Right
            directions.append((1, 0, "right"))
        if j > 0 and not self._cells[i][j - 1].visited:  # Up
            directions.append((0, -1, "top"))
        if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:  # Down
            directions.append((0, 1, "bottom"))

        random.shuffle(directions)  # Randomize traversal order

        for di, dj, direction in directions:
            ni, nj = i + di, j + dj
            neighbor = self._cells[ni][nj]

            if not neighbor.visited:
                # Remove walls between current cell and neighbor
                if direction == "left":
                    cell.has_left_wall = False
                    neighbor.has_right_wall = False
                elif direction == "right":
                    cell.has_right_wall = False
                    neighbor.has_left_wall = False
                elif direction == "top":
                    cell.has_top_wall = False
                    neighbor.has_bottom_wall = False
                elif direction == "bottom":
                    cell.has_bottom_wall = False
                    neighbor.has_top_wall = False

                self._draw_cell(i, j)
                self._draw_cell(ni, nj)

                # Recursively break walls from the new cell
                self._break_walls_r(ni, nj)

    def _reset_cells_visited(self):
        """Resets the visited property of all cells in the maze to False."""
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        """Starts the recursive solving process from (0,0). Returns True if a solution is found."""
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        """Recursively solves the maze using Depth-First Search (DFS)."""
        cell = self._cells[i][j]
        self._animate()  # Visualize each step

        if cell.visited:
            return False  # Already visited, don't revisit

        cell.visited = True  # Mark this cell as visited

        # Check if we've reached the goal (bottom-right corner)
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True  # Solution found!

        # Possible movement directions: (dx, dy, required_wall)
        directions = [
            (-1, 0, "left"),  # Left
            (1, 0, "right"),  # Right
            (0, -1, "top"),  # Up
            (0, 1, "bottom")  # Down
        ]

        for di, dj, wall in directions:
            ni, nj = i + di, j + dj  # New coordinates

            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows:  # Stay within bounds
                neighbor = self._cells[ni][nj]

                # Move if there's no wall blocking the path and the neighbor isn't visited
                if not neighbor.visited and not getattr(cell, f"has_{wall}_wall"):
                    cell.draw_move(neighbor)  # Draw the movement

                    if self._solve_r(ni, nj):  # Recursively solve
                        return True  # If solved, stop exploring

                    cell.draw_move(neighbor, undo=True)  # Undo move if dead-end

        return False  # No valid path from this cell
