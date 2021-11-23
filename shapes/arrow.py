from .shape import Shape


class Arrow(Shape):

    length = 50
    width = 1
    radius = 3
    color = "#000000"

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)

    def draw(self, x, y):
        self.drawer.ellipse((x-self.radius, y-self.radius, x+self.radius, y+self.radius), self.color)

        self.drawer.line((x, y, x, y+self.length), self.color, self.width)

        y = y + self.length
        self.drawer.line((x-5, y - 5, x, y), self.color, self.width)
        self.drawer.line((x, y, x+5, y-5), self.color, self.width)
