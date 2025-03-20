from window import Window
from maze import Maze

def main():
    win = Window(800, 600)  # Create the window
    maze = Maze(50, 50, 10, 10, 50, 50, win)  # Create a 10x10 maze

    maze.solve()  # Solve the maze!

    win.wait_for_close()  # Keep window open

if __name__ == "__main__":
    main()