from svgwrite.shapes import Ellipse, Line, Polyline
from .shape import Shape


class StraightArrow(Shape):

    radius = (3, 3)
    width = 1
    color = "#000000"

    def __init__(self, drawer, src: tuple, dst: tuple):
        super(StraightArrow, self).__init__(drawer)

        self.src = src
        self.x1 = src[0]
        self.y1 = src[1]

        self.dst = dst
        self.x2 = dst[0]
        self.y2 = dst[1]

    def draw(self):
        self.drawer.add(Ellipse(self.src, self.radius, fill=self.color))
        self.drawer.add(Line(self.src, self.dst, stroke=self.color, stroke_width=self.width))

        angle = self.get_angle((self.src, self.dst), ((0, 0), (0, -1)))
        if angle == 90:
            angle = -90
        self.drawer.add(Polyline([(self.x2 - 5, self.y2 + 5), self.dst, (self.x2 + 5, self.y2 + 5)],
                                 stroke=self.color, stroke_width=self.width, fill="none",
                                 transform=f"rotate({angle}, {self.x2}, {self.y2})"))
