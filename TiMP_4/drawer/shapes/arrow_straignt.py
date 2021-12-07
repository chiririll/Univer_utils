from .shape import Shape


class StraightArrow(Shape):

    width = 1
    radius = 3
    color = "#000000"

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)

    def draw(self, x1, y1, x2, y2):
        # Point
        self.drawer.ellipse((x1-self.radius, y1-self.radius, x1+self.radius, y1+self.radius), self.color)

        # Line
        self.drawer.line((x1, y1, x2, y2), self.color, self.width)

        # Arrow pointer
        self.drawer.line((x2-5, y2 - 5, x2, y2), self.color, self.width)
        self.drawer.line((x2, y2, x2+5, y2-5), self.color, self.width)
