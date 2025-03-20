from point import Point

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black"):
        """Draw the line on the given canvas with the specified color."""
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

    def __repr__(self):
        return f"Line({self.point1}, {self.point2})"