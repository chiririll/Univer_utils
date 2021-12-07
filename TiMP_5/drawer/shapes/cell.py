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
        pass

    def __paint_box(self):
        pass

    def __draw_text(self, text, type: str):
        text = str(text)
        pass

    def draw(self):
        self.__draw_box()
        return
        if self.cords[0] == 0:
            # Edge cell
            self.__paint_box()
            self.__draw_text()
        else:
            # Regular cell
            self.__draw_text()
            self.__draw_text()
            self.__draw_text()
