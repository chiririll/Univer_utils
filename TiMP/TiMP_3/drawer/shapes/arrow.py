from .shape import Shape


class Arrow(Shape):

    width = 1
    radius = 3
    color = "#000000"

    len_down = 20
    len_shift = 25

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)

    def draw(self, x1, y1, x2, y2, shift=0, ptr_type=0):
        
        direction = -1 if y2 > y1 else 1

        # Point
        self.drawer.ellipse((x1-self.radius, y1-self.radius, x1+self.radius, y1+self.radius), self.color)

        self.drawer.line((x1, y1, x1, y1 + self.len_down), self.color, self.width)

        y_dst = y1 + self.len_down + (self.len_down if direction < 0 else 0)
        self.drawer.line((x1, y1 + self.len_down, x1 + shift, y_dst), self.color, self.width)

        self.drawer.line(
            (x1 + shift, y_dst,
             x1 + shift, y2 + direction * self.len_shift),
            self.color, self.width
        )

        self.drawer.line(
            (x1 + shift, y2 + direction * self.len_shift,
             x2, y2),
            self.color, self.width
        )

        arrows = [
            ((x2 - 5, y2 - 5, x2, y2), (x2, y2, x2 + 5, y2 - 5)),   # \/
            ((x2, y2 - 5, x2, y2), (x2, y2, x2 + 5, y2)),
            ((x2 + 5, y2 - 5, x2, y2), (x2, y2, x2 + 5, y2 + 5)),   # <
            ((x2, y2, x2 + 5, y2), (x2, y2 + 5, x2, y2)),
            ((x2 + 5, y2 + 5, x2, y2), (x2, y2, x2 - 5, y2 + 5)),   # /\
            ((x2, y2 + 5, x2, y2), (x2 - 5, y2, x2, y2)),
            ((x2 - 5, y2 + 5, x2, y2), (x2, y2, x2 - 5, y2 - 5)),   # >
            ((x2 - 5, y2, x2, y2), (x2, y2, x2, y2-5)),
        ]
        self.drawer.line(arrows[ptr_type][0], self.color, self.width)
        self.drawer.line(arrows[ptr_type][1], self.color, self.width)
