from svgwrite.shapes import Rect

from .shape import Shape
from .arrow import Arrow
from .arrow_straight import StraightArrow
from .pointer import Pointer


class Cell(Shape):
    # Sizes
    size = (90, 34)
    spacing = 30
    padding = (20, 30)
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

    # Pointers
    ptr_base_angle = (10, 70)
    ptr_spacing = (w // 2, int(h / 2.8))
    ptr_spacing_angle = (0, 8)

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
        def check_cond(cond, num):
            if type(cond) is tuple:
                return cond[0] < num < cond[1]
            elif type(cond) is bool:
                return cond

        def get_free_sides():
            n = len(self.matrix.base_col)
            m = len(self.matrix.base_row)
            sides = {
                'right': ((0, 1), (-1, m-1), True),
                'left': ((0, -1), (0, m), True),
                'bottom': ((1, 0), True, (-1, n-1)),
                'top': ((-1, 0), True, (0, n)),
            }
            free = []

            i, j = self.el.get_cords()
            for name, conditions in sides.items():
                d, cond_x, cond_y = conditions
                if not self.matrix[i + d[0], j + d[1]] and check_cond(cond_x, j) and check_cond(cond_y, i):
                    free.append(name)
            return free

        def get_free_anchors(free_sides: list):
            points = []
            for side in free_sides:
                match side:
                    case 'bottom':
                        for i, x in enumerate(range(0, self.w, self.ptr_spacing[0])):
                            points.append({'pos': (x, self.h), 'angle': -180 - self.ptr_base_angle[0] - self.ptr_spacing_angle[0] * i})
                    case 'top':
                        for i, x in enumerate(range(0, self.w, self.ptr_spacing[0])):
                            points.append({'pos': (x, 0), 'angle': self.ptr_base_angle[0] + self.ptr_spacing_angle[0] * i})
                    case 'left':
                        for i, y in enumerate(range(self.ptr_spacing[1], self.h, self.ptr_spacing[1])):
                            points.append({'pos': (0, y), 'angle': -self.ptr_base_angle[1] - self.ptr_spacing_angle[1] * i})
                    case 'right':
                        for i, y in enumerate(range(0, self.h, self.ptr_spacing[1])):
                            points.append({'pos': (self.w, y), 'angle': self.ptr_base_angle[1] + self.ptr_spacing_angle[1] * i})

            if self.cords[1] < len(self.matrix.base_col) - 1:
                points.append({'pos': (self.w, self.h), 'angle': 45 + self.ptr_base_angle[1]})
                points.append({'pos': (self.w, 0), 'angle': self.ptr_base_angle[1]})
            if self.cords[1] > 0:
                points.append({'pos': (0, self.h), 'angle': -45 - self.ptr_base_angle[1]})
                points.append({'pos': (0, 0), 'angle': -self.ptr_base_angle[1]})

            return points

        if not self.pointers:
            return

        params = get_free_anchors(get_free_sides())
        for ptr in self.pointers:
            param = params.pop(0)
            Pointer(self.drawer, self.get_c(param['pos']), ptr, angle=param['angle']).draw()

    def __draw_arrows(self):
        # Left
        if self.el.left:
            target = Cell.get_pos(self.el.left)
            params = (self.drawer, self.get_c('arrow_left'), (target[0] + self.w, target[1] + self.arrow_left[1]))
            if self.cords[1] <= self.el.left[1]:
                Arrow(*params).draw()
            else:
                shift = 15 if self.matrix.find_next(self.cords, 0) != self.el.left else 0
                StraightArrow(*params, shift=shift).draw()
        # Up
        if self.el.up:
            target = Cell.get_pos(self.el.up)
            params = (self.drawer, self.get_c('arrow_up'), (target[0] + self.arrow_up[0], target[1] + self.h))
            if self.cords[0] <= self.el.up[0]:
                Arrow(*params, angle=90).draw()
            else:
                shift = 30 if self.matrix.find_next(self.cords, 1) != self.el.up else 0
                StraightArrow(*params, shift=shift).draw()

    def draw(self):
        self.__draw_box()

        if self.el.val is None:
            # Edge cell
            self.__draw_text(-1, 'row' if self.cords[0] == 0 else 'col')
        elif self.el.draw_text:
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
