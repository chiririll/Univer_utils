import math

from svgwrite.shapes import Polyline, Line

from .shape import Shape


class Pointer(Shape):

    width = 1

    def __init__(self, drawer, pos: tuple, text="P", index: bool = False, angle: int = 45, length: int = 20, draw_arrow: bool = True):
        a_rad = math.radians(angle)
        l = (length + len(text) * 5,
             length + 14)

        text_c = (round(math.sin(a_rad) * l[0]), -round(math.cos(a_rad) * l[1]) + 5)
        text_index = (text_c[0] + 5, text_c[1] + 2)

        self.text = str(text)
        self.index = index
        self.angle = angle
        self.length = length
        self.draw_arrow = draw_arrow

        super(Pointer, self).__init__(drawer, pos=pos, text_c=text_c, text_index=text_index)

    def draw(self):
        if self.draw_arrow:
            self.drawer.add(Polyline([(self.x - 5, self.y - 5), self.pos, (self.x + 5, self.y - 5)],
                                     stroke=self.color, stroke_width=self.width, fill="none",
                                     transform=f"rotate({self.angle}, {self.x}, {self.y})"))
            self.drawer.add(Line((self.x, self.y - self.length), self.pos, stroke=self.color, stroke_width=self.width,
                                 transform=f"rotate({self.angle}, {self.x}, {self.y})"))

        self.drawer.add(self.drawer.text(self.text[0] if self.index else self.text, self.get_c('text_c'),
                                         style=self.text_style, alignment_baseline="middle", text_anchor="middle",
                                         font_style="italic"))
        if self.index:
            self.drawer.add(self.drawer.text(self.text[1:], self.get_c('text_index'), style=self.text_style_index,
                                             alignment_baseline="middle", text_anchor="start", font_style="normal"))
