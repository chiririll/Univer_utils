from svgwrite.shapes import Rect, Line

from .shape import Shape
from .arrow import Arrow
from .arrow_straight import StraightArrow
from .pointer import Pointer


class Cell(Shape):
    # Sizes
    size = (90, 34)
    spacing = 30
    padding = (30, 20)
    w = size[0]
    h = size[1]

    # Colors
    col_line = "#000000"
    col_fill = "#bbbbbb"
    col_text = "#000000"

    # Arrows
    arrow_left = (w // 4, h // 4)
    arrow_up = (w // 4 * 3, h // 4)

    # Text
    text_cols = [
        'row',
        'col',
        'val'
    ]

    def __init__(self, drawer, matrix, element, pointers: list = None):
        self.matrix = matrix
        self.el = element
        self.cords = element.get_cords()
        self.pointers = pointers

        self.pos = self.get_pos(self.cords)
        self.x = self.pos[0]
        self.y = self.pos[1]

        super(Cell, self).__init__(drawer, pos=self.pos, arrow_left=self.arrow_left, arrow_up=self.arrow_up, ptr=(self.w, 0))

    def __draw_box(self):
        self.drawer.add(Rect(self.pos, self.size, fill="#ffffff", stroke=self.col_line))

        for i in range(2):
            fill = "none"
            if self.cords[0] == 0 and i != 1 or self.cords[1] == 0 and i != 0:
                fill = self.col_fill
            self.drawer.add(Rect(
                (self.x + self.w // 2 * i, self.y),
                (self.w // 2, self.h // 2),
                fill=fill, stroke=self.col_line)
            )

        for i in range(3):
            fill = "none"
            if self.cords[1] == 0 and i != 1 or self.cords[0] == 0 and i != 0:
                fill = self.col_fill
            self.drawer.add(Rect(
                (self.x + self.w // 3 * i, self.y + self.h // 2),
                (self.w // 3, self.h // 2),
                fill=fill, stroke=self.col_line)
            )

    def __draw_text(self, text, t_type: str):
        text = str(text)

        col = self.text_cols.index(t_type)
        pos = (self.x + self.w // 3 * col + self.w // 6, self.y + self.h // 2 + self.h // 4 + 5)
        self.drawer.add(self.drawer.text(text, pos, style=self.text_style, alignment_baseline="middle", text_anchor="middle"))

    def __draw_pointers(self):
        if not self.pointers:
            return
        for ptr in self.pointers:
            Pointer(self.drawer, self.get_c('ptr'), ptr, angle=70).draw()

    def __draw_arrows(self):
        # Left
        if self.el.left:
            target = Cell.get_pos(self.el.left)
            params = (self.drawer, self.get_c('arrow_left'), (target[0] + self.w, target[1] + self.arrow_left[1]))
            if self.cords[1] <= self.el.left[1]:
                Arrow(*params).draw()
            else:
                StraightArrow(*params).draw()
        # Up
        if self.el.up:
            target = Cell.get_pos(self.el.up)
            params = (self.drawer, self.get_c('arrow_up'), (target[0] + self.arrow_up[0], target[1] + self.h))
            StraightArrow(*params).draw()
            if self.cords[0] <= self.el.up[1]:
                Arrow(*params)#.draw()
            else:
                StraightArrow(*params).draw()

    def draw(self):
        self.__draw_box()

        if not self.el.val:
            # Edge cell
            self.__draw_text(-1, 'row' if self.cords[0] == 0 else 'col')
        else:
            # Regular cell
            self.__draw_text(self.cords[0], 'row')
            self.__draw_text(self.cords[1], 'col')
            self.__draw_text(self.el.val, 'val')

        self.__draw_arrows()
        self.__draw_pointers()

    @staticmethod
    def get_pos(cords: tuple) -> tuple:
        x = Cell.padding[1] + cords[1] * Cell.w + cords[1] * Cell.spacing
        y = Cell.padding[0] + cords[0] * Cell.h + cords[0] * Cell.spacing
        return x, y
