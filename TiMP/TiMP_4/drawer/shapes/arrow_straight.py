from svgwrite.shapes import Ellipse, Polyline
from .shape import Shape


class StraightArrow(Shape):

    radius = (3, 3)
    width = 1
    color = "#000000"

    offset = 10  # Shift length (shift = length / offset)

    def __init__(self, drawer, src: tuple, dst: tuple, shift=0):
        super(StraightArrow, self).__init__(drawer)

        self.shift = shift

        self.src = src
        self.x1 = src[0]
        self.y1 = src[1]

        self.dst = dst
        self.x2 = dst[0]
        self.y2 = dst[1]

    def draw(self):
        def get_multiline(src: tuple, dst: tuple, shift: int, length: int) -> list:
            """
            Function for getting multiline points
            :param src: Start point
            :param dst: End point
            :param shift: Line shift
            :return: List of points
            """
            x1, y1 = src
            x2, y2 = dst
            offset = length // self.offset
            return [
                src,
                (x1, y1 - offset // 2),
                (x1 + shift, y1 - offset),
                (x2 + shift, y2 + offset),
                (x2, y2 + offset // 2),
                dst
            ]

        angle = self.get_angle((self.src, self.dst), ((0, 0), (0, -1)))

        self.drawer.add(Ellipse(self.src, self.radius, fill=self.color))
        length = int(self.get_distance(self.src, self.dst))
        self.drawer.add(Polyline(get_multiline(self.src, (self.x1, self.y1 - length), self.shift, length), stroke=self.color,
                                 stroke_width=self.width, fill="none", transform=f"rotate({angle}, {self.x1}, {self.y1})"))

        self.drawer.add(Polyline([(self.x2 - 5, self.y2 + 5), self.dst, (self.x2 + 5, self.y2 + 5)],
                                 stroke=self.color, stroke_width=self.width, fill="none",
                                 transform=f"rotate({angle}, {self.x2}, {self.y2})"))
