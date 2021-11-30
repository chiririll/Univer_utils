from PIL import ImageFont

from .shape import Shape


class Pointer(Shape):
    color = "#000000"
    width = 2
    length = 10
    font_size = 14

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)
        self.pos = kwargs.get('pos', (0, 0))

    def draw(self, x, y):
        self.drawer.line((x, y, x-5, y), self.color, self.width)
        self.drawer.line((x, y, x, y-5), self.color, self.width)

        self.drawer.line((x, y, x-self.length, y-self.length), self.color, self.width)

        font = ImageFont.truetype("src/timesnewroman.ttf", self.font_size)
        self.drawer.text((x-self.length-self.font_size+5, y-self.length-self.font_size), 'P', self.color, font)
