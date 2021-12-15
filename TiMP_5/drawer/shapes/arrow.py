from svgwrite.shapes import Ellipse, Polyline, Line

from .shape import Shape


class Arrow(Shape):

    point_radius = (3, 3)
    shift = ((30, 20), (-15, 20))
    shift_90 = ((20, 35), (-15, 35))

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
        def draw_loop(x, y, sx, sy, angle=0):
            points = [
                (x, y),
                (x - sx // 2, y),
                (x - sx, y - sy // 3),
                (x - sx, y - sy // 3 * 2),
                (x - sx // 2, y - sy),
                (x, y - sy)
            ]
            self.drawer.add(Polyline(points, stroke=self.color, stroke_width=self.width, fill="none",
                                     transform=f"rotate({angle}, {x}, {y})"))

        def draw_line(pos, s):
            cords = []
            for i in range(2):
                cords.append((pos[i][0], pos[i][1] - s[i][1]) if self.angle == 0 else (pos[i][0] + s[i][1], pos[i][1]))
            self.drawer.add(Line(*cords, stroke=self.color, stroke_width=self.width, fill="none"))

        def draw_arrow(x, y, angle):
            self.drawer.add(Polyline([(x - 5, y + 5), (x, y), (x + 5, y + 5)],
                                     stroke=self.color, stroke_width=self.width, fill="none",
                                     transform=f"rotate({angle}, {x}, {y})"))

        def get_shift():
            if self.angle == 0:
                return self.shift
            return self.shift_90

        self.drawer.add(Ellipse(self.src, self.point_radius, fill=self.color))

        draw_loop(*self.src, *get_shift()[0], self.angle)
        draw_line((self.src, self.dst), get_shift())
        draw_loop(*self.dst, *get_shift()[1], self.angle)

        draw_arrow(*self.dst, self.angle - 90)
