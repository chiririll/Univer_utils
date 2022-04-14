from svgwrite.shapes import Line, Ellipse

from .shape import Shape


class Ground(Shape):

    offset = (25, 20)
    radius = (3, 3)
    width = 1
    size = 3

    def __init__(self, drawer, pos: tuple):

        super(Ground, self).__init__(drawer, pos=pos)

    def draw(self):
        self.drawer.add(Ellipse(self.pos, self.radius, fill=self.color))
        self.drawer.add(
            Line(self.pos, (self.pos[0] + self.offset[0], self.pos[1]), stroke=self.color, stroke_width=self.width))
        self.drawer.add(
            Line((self.pos[0] + self.offset[0], self.pos[1]), (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]),
                 stroke=self.color, stroke_width=self.width))

        for i in range(3):
            x = self.pos[0] + self.offset[0]
            y = self.pos[1] + self.offset[1] - i * self.size
            self.drawer.add(
                Line((x - (i + 1) * self.size, y), (x + (i + 1) * self.size, y), stroke=self.color, stroke_width=self.width))
