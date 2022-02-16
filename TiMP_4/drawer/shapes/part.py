from svgwrite.shapes import Rect, Line

from .shape import Shape
from .arrow import Arrow
from .arrow_straight import StraightArrow
from .pointer import Pointer


class Part(Shape):
    # Sizes
    size = (18, 18)     # Cell size
    w = size[0]
    h = size[1]

    # Colors
    col_line = "#000000"
    col_text = "#000000"

    # Arrow
    arrow_pos = (4.5 * w, 0.5 * h)

    # Pointers
    ptr_spacing = w * 2

    def __init__(self, drawer, pos, part: list, pointers: list = None):
        self.part = part

        if pointers is None:
            pointers = []
        self.pointers = pointers

        super(Part, self).__init__(drawer, pos=pos, arrow=self.arrow_pos)

    def __draw_box(self):
        self.drawer.add(Rect(self.pos, (self.w * 5, self.h), fill="#ffffff", stroke=self.col_line))

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
        # TODO: Fix indices
        for i, ptr in enumerate(self.pointers):
            pos = (self.x + self.ptr_spacing * i, self.y)
            Pointer(self.drawer, pos, ptr, angle=-45).draw()

    def draw(self):
        self.__draw_box()

        for i in range(4):
            self.__draw_text(self.part[i], i)

        self.__draw_pointers()

    def get_arrow(self):
        return self.get_c('arrow')
