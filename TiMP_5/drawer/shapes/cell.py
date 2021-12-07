from svgwrite.shapes import Rect, Line

from .shape import Shape


class Cell(Shape):
    # Sizes
    size = (150, 50)
    spacing = 30
    w = size[0]
    h = size[1]

    # Colors
    col_line = "#000000"
    col_fill = "#aaaaaa"
    col_text = "#000000"

    # Text
    text_types = {
        'row': (),
        'col': (),
        'val': ()
    }

    def __init__(self, drawer, matrix, cords):
        super(Cell, self).__init__(drawer)

        self.matrix = matrix
        self.cords = cords

        self.x = cords[0] * self.w + cords[0] * self.spacing
        self.y = cords[1] * self.h + cords[1] * self.spacing
        self.pos = (self.x, self.y)

    def __draw_box(self):
        self.drawer.add(Rect(self.pos, self.size, fill="#ffffff", stroke=self.col_line))

        self.drawer.add(Line((self.x, self.y + self.h // 2), (self.x + self.w, self.y + self.h // 2), stroke=self.col_line))

        for i in range(1, 3):
            x = self.x + self.w // 3 * i
            self.drawer.add(Line((x, self.y + self.h // 2), (x, self.y + self.h), stroke=self.col_line))

    def __paint_box(self):
        pass

    def __draw_text(self, text, type: str):
        text = str(text)
        text_style = "font-size:%ipt; font-family:%s" % (14, "Times New Roman")
        pos = self.text_types[type]
        self.drawer.add(self.drawer.text(text, pos, style=text_style))
        pass

    def draw(self):
        self.__draw_box()

        if self.cords[0] == 0 or self.cords[1] == 0:
            # Edge cell
            self.__paint_box()
            self.__draw_text(-1, 'row' if self.cords[0] == 0 else 'col')
        else:
            # Regular cell
            self.__draw_text(self.cords[0], 'row')
            self.__draw_text(self.cords[1], 'col')
            self.__draw_text("val", 'val')
