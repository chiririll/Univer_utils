from .shape import Shape


class Arrow(Shape):

    width = 1
    radius = 3
    color = "#000000"

    len_start = 20
    len_shift = 20

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)

    def draw(self, x1, y1, x2, y2, shift=0):
        len_start = 45-shift
        len_shift = 15 + len_start

        self.drawer.ellipse((x1-self.radius, y1-self.radius, x1+self.radius, y1+self.radius), self.color)

        self.drawer.line((x1, y1, x1, y1 + len_start), self.color, self.width)
        self.drawer.line((x1, y1 + len_start, x1 + shift, y1 + len_shift), self.color, self.width)

        self.drawer.line((x1 + shift, y1 + len_shift, x2 + shift, y2 - len_shift), self.color, self.width)

        self.drawer.line((x2 + shift, y2 - len_shift, x2, y2 - len_start), self.color, self.width)
        self.drawer.line((x2, y2 - len_start, x2, y2), self.color, self.width)

        # TODO: rotate ending
        self.drawer.line((x2-5, y2 - 5, x2, y2), self.color, self.width)
        self.drawer.line((x2, y2, x2+5, y2-5), self.color, self.width)
