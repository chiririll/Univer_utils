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

    # Pointers
    ptr_base_angle = (10, 65)
    ptr_spacing = (int(w / 2.5), h // 3)
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
        def get_free_sides():
            sides = {
                'right': (0, 1),
                'bottom': (1, 0),
                'left': (0, -1),
                'top': (-1, 0),
            }
            free = []

            i, j = self.el.get_cords()
            for name, d in sides.items():
                if not self.matrix[i + d[0], j + d[1]] and i > 0 and j > 0:
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

            points.append({'pos': (self.w, self.h), 'angle': 110})
            if self.cords[0] == 0:
                points.append({'pos': (0, self.h), 'angle': -110})
            elif self.cords[1] == 0:
                points.append({'pos': (self.w, 0), 'angle': 70})
            else:
                points.append({'pos': (0, 0), 'angle': -70})

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
                StraightArrow(*params).draw()
        # Up
        if self.el.up:
            target = Cell.get_pos(self.el.up)
            params = (self.drawer, self.get_c('arrow_up'), (target[0] + self.arrow_up[0], target[1] + self.h))
            if self.cords[0] <= self.el.up[0]:
                Arrow(*params, angle=90).draw()
            else:
                # TODO: check neighbours
                StraightArrow(*params).draw()

    def draw(self):
        self.__draw_box()

        if not self.el.val:
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
