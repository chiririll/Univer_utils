from .shape import Shape


class Ground(Shape):

    length = 25
    width = 1
    radius = 3
    color = "#000000"

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)

    def draw(self, x, y):
        self.drawer.ellipse((x-self.radius, y-self.radius, x+self.radius, y+self.radius), self.color)

        self.drawer.line((x, y, x, y+self.length), self.color, self.width)

        y = y + self.length
        for i in range(3):
            self.drawer.line((x - 2*i - 3, y - 3*i, x + 2*i + 3, y - 3*i), self.color, self.width)
