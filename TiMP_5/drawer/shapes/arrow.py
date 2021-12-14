from svgwrite.shapes import Ellipse, Polyline

from .shape import Shape


class Arrow(Shape):

    point_radius = (3, 3)
    shift = ((30, 20), (15, 20))

    width = 1

    def __init__(self, drawer, src: tuple, dst: tuple, angle: int = 0, shift: tuple = None, vertical=False):
        super(Arrow, self).__init__(drawer)

        if shift:
            self.shift = shift
        self.angle = angle

        self.src = src
        self.x1 = src[0] if not vertical else src[1]
        self.y1 = src[1] if not vertical else src[0]

        self.dst = dst
        self.x2 = dst[0] if not vertical else dst[1]
        self.y2 = dst[1] if not vertical else dst[0]

    def draw(self):
        self.drawer.add(Ellipse(self.src, self.point_radius, fill=self.color))

        points = [
            self.src,
            (self.x1 - self.shift[0][0] // 2, self.y1),
            (self.x1 - self.shift[0][0], self.y1 - self.shift[0][1] // 3),
            (self.x1 - self.shift[0][0], self.y1 - self.shift[0][1] // 3 * 2),
            (self.x1 - self.shift[0][0] // 2,  self.y1 - self.shift[0][1]),

            (self.x1, self.y1 - self.shift[0][1]),
            (self.x2, self.y2 - self.shift[1][1]),

            (self.x2 + self.shift[1][0] // 2, self.y1 - self.shift[1][1]),
            (self.x2 + self.shift[1][0], self.y1 - self.shift[1][1] // 3 * 2),
            (self.x2 + self.shift[1][0], self.y1 - self.shift[1][1] // 3),
            (self.x2 + self.shift[1][0] // 2, self.y1),
            self.dst
        ]
        self.drawer.add(Polyline(points, stroke=self.color, stroke_width=self.width, fill="none"))

        angle = 270
        self.drawer.add(Polyline([(self.x2 - 5, self.y2 + 5), self.dst, (self.x2 + 5, self.y2 + 5)],
                                 stroke=self.color, stroke_width=self.width, fill="none",
                                 transform=f"rotate({angle}, {self.x2}, {self.y2})"))
