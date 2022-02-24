from svgwrite.shapes import Rect, Line

from .shape import Shape
from .pointer import Pointer


class Card(Shape):
    # Sizes
    size = (22, 18)     # Cell size
    cells = 4           # Cell count
    w = size[0]
    h = size[1]

    # Colors
    col_line = "#000000"
    col_text = "#000000"

    # Arrow
    arrow_pos = ((cells - 0.5) * w, 0.5 * h)

    # Pointers
    ptr_spacing = w * 2

    def __init__(self, drawer, pos, card: dict, pointers: list = None):
        self.card = card

        if pointers is None:
            pointers = []
        self.pointers = pointers

        super(Card, self).__init__(drawer, pos=pos, arrow=self.arrow_pos)

    def __draw_box(self):
        self.drawer.add(Rect(self.pos, (self.w * self.cells, self.h), fill="#ffffff", stroke=self.col_line))

        for i in range(1, 5):
            x_pos = self.x + i * self.w
            self.drawer.add(Line((x_pos, self.y), (x_pos, self.y + self.h), stroke=self.col_line))

    def __draw_text(self, text, index: int):
        if text is None:
            return
        text = str(text)

        pos = (
            self.x + self.w * index + self.w // 2,
            self.y + self.h * .7
        )
        self.drawer.add(self.drawer.text(text, pos, style=self.text_style, alignment_baseline="middle", text_anchor="middle"))

    def __draw_pointers(self):
        for i, ptr in enumerate(self.pointers):
            pos = (self.x + self.ptr_spacing * i, self.y)
            Pointer(self.drawer, pos, ptr, angle=-45).draw()

    def draw(self):
        self.__draw_box()

        params = [
            self.card['TAG'],
            self.card['SUIT'],
            self.card['RANK']
        ]

        for i, text in enumerate(params):
            self.__draw_text(text, i)

        self.__draw_pointers()

    def get_arrow(self):
        return self.get_c('arrow')

    @staticmethod
    def get_size():
        return Card.cells * Card.w, Card.h
