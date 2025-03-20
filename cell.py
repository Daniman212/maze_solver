from point import Point
from line import Line
from window import Window

class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, win=None):
        """Initialize a cell with its top-left (x1, y1) and bottom-right (x2, y2) coordinates."""
        self._x1, self._y1 = x1, y1
        self._x2, self._y2 = x2, y2
        self._win = win  # Reference to the window

        # By default, all walls exist
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        # New: Track if this cell has been visited in maze generation
        self.visited = False

    def draw(self):
        """Draws the cell's walls. If a wall is removed, it is drawn in white to visually erase it."""
        bg_color = "#d9d9d9"  # Default Tkinter background color

        if self._win:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
                                "black" if self.has_left_wall else bg_color)
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
                                "black" if self.has_right_wall else bg_color)
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
                                "black" if self.has_top_wall else bg_color)
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
                                "black" if self.has_bottom_wall else bg_color)


    def draw_move(self, to_cell, undo=False):
        """Draws a path between two cells. Red for movement, gray for backtracking."""
        color = "gray" if undo else "red"
        start_x = (self._x1 + self._x2) // 2  # Center of current cell
        start_y = (self._y1 + self._y2) // 2
        end_x = (to_cell._x1 + to_cell._x2) // 2  # Center of target cell
        end_y = (to_cell._y1 + to_cell._y2) // 2

        self._win.draw_line(Line(Point(start_x, start_y), Point(end_x, end_y)), color)

    def __repr__(self):
        return f"Cell(({self._x1}, {self._y1}) to ({self._x2}, {self._y2}))"