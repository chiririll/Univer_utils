from PIL import ImageFont

from .shape import Shape
from .pointer import Pointer


class Cell(Shape):
    size = (30, 60)
    width = 1
    color = "#000000"

    k_pos = (10, -20)
    count_pos = (10, 5)
    font_size = 14

    link = (15, 45)

    def __init__(self, drawer, **kwargs):
        super().__init__(drawer)

        self.k = kwargs.get('k', "")
        self.count = kwargs.get('count', "")
        self.pos = kwargs.get('pos', (0, 0))

        self.font = ImageFont.truetype("src/timesnewroman.ttf", self.font_size)

    def draw(self, **kwargs):
        x = self.pos[0]
        y = self.pos[1]

        # Lines #
        self.drawer.line((x, y, x, y + self.size[1]), self.color, self.width)
        self.drawer.line((x + self.size[0], y, x + self.size[0], y + self.size[1]), self.color, self.width)

        self.drawer.line((x, y + self.size[1] // 2, x + self.size[0], y + self.size[1] // 2), self.color, self.width)

        self.drawer.line((x, y, x + self.size[0], y), self.color, self.width)
        self.drawer.line((x, y + self.size[1], x + self.size[0], y + self.size[1]), self.color, self.width)
        # ===== #

        # Text #
        if kwargs.get('draw_count', True):
            self.draw_count()
        if kwargs.get('draw_k', True):
            self.draw_k()
        # ==== #

    def draw_count(self):
        x = self.pos[0]
        y = self.pos[1]
        self.drawer.text((x + self.count_pos[0], y + self.count_pos[1]), self.count, self.color, self.font)

    def draw_k(self):
        x = self.pos[0]
        y = self.pos[1]
        self.drawer.text((x + self.k_pos[0], y + self.k_pos[1]), self.k, self.color, self.font)

    def draw_link(self, drawer, link: Shape):
        x = self.pos[0] + self.link[0]
        y = self.pos[1] + self.link[1]
        link.draw(x=x, y=y)

    def draw_pointer(self):
        ptr = Pointer(self.drawer)
        ptr.draw(self.pos[0], self.pos[1])
