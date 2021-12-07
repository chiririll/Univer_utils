from svgwrite.shapes import Rect, Line

from .arrow_straight import StraightArrow
from .shape import Shape


class Cell(Shape):
    # Sizes
    size = (150, 50)
    spacing = 30
    padding = (30, 30)
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
    text_types = {
        'row': (15, 43),
        'col': (70, 43),
        'val': (115, 43)
    }

    def __init__(self, drawer, matrix, cords):
        self.matrix = matrix
        self.cords = cords
        self.el = matrix.get(cords)

        self.x = self.padding[1] + cords[1] * self.w + cords[1] * self.spacing
        self.y = self.padding[0] + cords[0] * self.h + cords[0] * self.spacing
        self.pos = (self.x, self.y)

        super(Cell, self).__init__(drawer, pos=self.pos, arrow_left=self.arrow_left, arrow_up=self.arrow_up)

    def __draw_box(self):
        self.drawer.add(Rect(self.pos, self.size, fill="#ffffff", stroke=self.col_line))

        self.drawer.add(Line((self.x + self.w // 2, self.y), (self.x + self.w // 2, self.y + self.h // 2), stroke=self.col_line))
        self.drawer.add(Line((self.x, self.y + self.h // 2), (self.x + self.w, self.y + self.h // 2), stroke=self.col_line))

        for i in range(1, 3):
            x = self.x + self.w // 3 * i
            self.drawer.add(Line((x, self.y + self.h // 2), (x, self.y + self.h), stroke=self.col_line))

    def __paint_box(self):
        stroke = 1
        rects = []

        rects.append((
            (self.x + self.w // 3 * 2 + stroke, self.y + self.h // 2 + stroke),
            (self.w // 3 - stroke*2, self.h // 2 - stroke*2)
        ))

        if self.cords[0] == 0:
            rects.append((
                (self.x + self.w // 3 + stroke, self.y + self.h // 2 + stroke),
                (self.w // 3 - stroke*2, self.h // 2 - stroke*2)
            ))
            rects.append((
                (self.x + stroke, self.y + stroke),
                (self.w // 2 - stroke*2, self.h // 2 - stroke*2)
            ))
        else:
            rects.append((
                (self.x + stroke, self.y + self.h // 2 + stroke),
                (self.w // 3 - stroke*2, self.h // 2 - stroke*2)
            ))
            rects.append((
                (self.x + self.w // 2 + stroke, self.y + stroke),
                (self.w // 2 - stroke * 2, self.h // 2 - stroke * 2)
            ))

        for rect in rects:
            self.drawer.add(Rect(*rect, fill=self.col_fill))

    def __draw_text(self, text, t_type: str):
        text = str(text)
        text_style = "font-size:%ipt; font-family:%s" % (14, "Times New Roman")
        # TODO: center
        pos = (self.x + self.text_types[t_type][0], self.y + self.text_types[t_type][1])
        self.drawer.add(self.drawer.text(text, pos, style=text_style))
        pass

    def draw(self):
        self.__draw_box()

        if not self.el:
            # Edge cell
            self.__paint_box()
            self.__draw_text(-1, 'row' if self.cords[0] == 0 else 'col')
        else:
            # Regular cell
            self.__draw_text(self.cords[0], 'row')
            self.__draw_text(self.cords[1], 'col')
            self.__draw_text(self.el, 'val')

        StraightArrow(self.drawer, self._get_c('arrow_left'), self._get_c('arrow_up')).draw()
