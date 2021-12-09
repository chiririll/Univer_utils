import math

from svgwrite.shapes import Polyline, Line

from .shape import Shape


class Pointer(Shape):

    def __init__(self, drawer, pos: tuple, text="P", angle: int = 45, length: int = 30):
        a_rad = math.radians(angle)
        l = length + 14
        text_c = (round(math.sin(a_rad) * l), -round(math.cos(a_rad) * l))

        super(Pointer, self).__init__(drawer, pos=pos, text_c=text_c)

        self.text = str(text)
        self.angle = angle
        self.length = length

    def draw(self):
        self.drawer.add(Polyline([(self.x - 5, self.y - 5), self.pos, (self.x + 5, self.y - 5)],
                                 stroke=self.color, stroke_width=self.width, fill="none",
                                 transform=f"rotate({self.angle}, {self.x}, {self.y})"))
        self.drawer.add(Line((self.x, self.y - self.length), self.pos, stroke=self.color, stroke_width=self.width,
                             transform=f"rotate({self.angle}, {self.x}, {self.y})"))

        self.drawer.add(self.drawer.text(self.text, self._get_c('text_c'), style=self.text_style,
                                         alignment_baseline="middle", text_anchor="middle"))
