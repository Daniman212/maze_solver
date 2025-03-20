import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_different_sizes(self):
        """Test maze with different numbers of rows and columns."""
        m2 = Maze(0, 0, 5, 5, 10, 10)
        self.assertEqual(len(m2._cells), 5)
        self.assertEqual(len(m2._cells[0]), 5)

        m3 = Maze(0, 0, 20, 15, 10, 10)
        self.assertEqual(len(m3._cells), 15)
        self.assertEqual(len(m3._cells[0]), 20)

    def test_maze_zero_size(self):
        """Test that a maze with zero rows or columns creates no cells."""
        m4 = Maze(0, 0, 0, 0, 10, 10)
        self.assertEqual(len(m4._cells), 0)

    def test_maze_single_cell(self):
        """Test a 1x1 maze."""
        m5 = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m5._cells), 1)
        self.assertEqual(len(m5._cells[0]), 1)

    def test_break_entrance_and_exit(self):
        """Ensure entrance and exit walls are removed correctly."""
        m6 = Maze(0, 0, 5, 5, 10, 10)

        # Top-left cell should NOT have a top wall
        self.assertFalse(m6._cells[0][0].has_top_wall)

        # Bottom-right cell should NOT have a bottom wall
        self.assertFalse(m6._cells[m6._num_cols - 1][m6._num_rows - 1].has_bottom_wall)

    def test_reset_cells_visited(self):
        """Ensure _reset_cells_visited resets all visited properties to False."""
        m = Maze(0, 0, 5, 5, 10, 10, seed=42)  # Generate a fixed 5x5 maze

        # Manually set all cells to visited (simulating a solve process)
        for i in range(m._num_cols):
            for j in range(m._num_rows):
                m._cells[i][j].visited = True

        # Call the reset method
        m._reset_cells_visited()

        # Check that all cells are reset to False
        for i in range(m._num_cols):
            for j in range(m._num_rows):
                self.assertFalse(m._cells[i][j].visited, f"Cell ({i},{j}) was not reset!")

if __name__ == "__main__":
    unittest.main()
