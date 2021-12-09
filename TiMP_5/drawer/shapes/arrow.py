from svgwrite.shapes import Ellipse, Polyline

from .shape import Shape


class Arrow(Shape):

    point_radius = (3, 3)
    shift = (50, 30)

    def __init__(self, drawer, src: tuple, dst: tuple):
        super(Arrow, self).__init__(drawer)

        self.src = src
        self.x1 = src[0]
        self.y1 = src[1]

        self.dst = dst
        self.x2 = dst[0]
        self.y2 = dst[1]

    def draw(self):
        self.drawer.add(Ellipse(self.src, self.point_radius, fill=self.color))

        points = [
            self.src,
            (self.x1 - self.shift[0] // 2, self.y1),
            (self.x1 - self.shift[0], self.y1 - self.shift[1] // 3),
            (self.x1 - self.shift[0], self.y1 - self.shift[1] // 3 * 2),
            (self.x1 - self.shift[0] // 2,  self.y1 - self.shift[1]),

            (self.x1, self.y1 - self.shift[1]),
            (self.x2, self.y2 - self.shift[1]),

            (self.x2 + self.shift[0] // 2, self.y1 - self.shift[1]),
            (self.x2 + self.shift[0], self.y1 - self.shift[1] // 3 * 2),
            (self.x2 + self.shift[0], self.y1 - self.shift[1] // 3),
            (self.x2 + self.shift[0] // 2, self.y1),
            self.dst
        ]
        self.drawer.add(Polyline(points, stroke=self.color, stroke_width=self.width, fill="none"))

        angle = 270
        self.drawer.add(Polyline([(self.x2 - 5, self.y2 + 5), self.dst, (self.x2 + 5, self.y2 + 5)],
                                 stroke=self.color, stroke_width=self.width, fill="none",
                                 transform=f"rotate({angle}, {self.x2}, {self.y2})"))
