from PIL import ImageFont

from .shape import Shape
from .pointer import Pointer
from .ground import Ground
from .arrow_straignt import StraightArrow
from .arrow import Arrow


class Cell(Shape):
    size = (30, 40)
    width = 1
    color = "#000000"
    selection_color = "#00dd00"

    k_pos = (12, -20)
    count_pos = (12, 3)
    font_size = 14
    cell_spacing = 70

    link = (15, 30)

    def __init__(self, drawer, node, pos):
        super().__init__(drawer)

        self.node = node
        self.pos = pos
        self.font = ImageFont.truetype("/times.ttf", self.font_size)

    def __draw_box(self, x, y):
        self.drawer.line((x, y, x, y + self.size[1]), self.color, self.width)
        self.drawer.line((x + self.size[0], y, x + self.size[0], y + self.size[1]), self.color, self.width)

        self.drawer.line((x, y + self.size[1] // 2, x + self.size[0], y + self.size[1] // 2), self.color, self.width)

        self.drawer.line((x, y, x + self.size[0], y), self.color, self.width)
        self.drawer.line((x, y + self.size[1], x + self.size[0], y + self.size[1]), self.color, self.width)

    def __draw_count(self, x, y):
        if self.node.count is None and self.node.qlink is None:
            return

        text = self.node.count
        if self.node.qlink:
            text = self.node.qlink
            self.drawer.rectangle(
                (x + self.count_pos[0] - 1, y + self.count_pos[1],
                 x + self.count_pos[0] + self.font_size * 0.5, y + self.count_pos[1] + self.font_size),
                self.selection_color
            )
        self.drawer.text((x + self.count_pos[0], y + self.count_pos[1]), str(text), self.color, self.font)

    def __draw_index(self, x, y):
        if self.node.k is not None:
            self.drawer.text((x + self.k_pos[0], y + self.k_pos[1]), str(self.node.k), self.color, self.font)

    def __draw_pointer(self):
        if not self.node.ptr:
            return
        ptr = Pointer(self.drawer)
        ptr.draw(self.pos[0], self.pos[1])

    def draw(self, **kwargs):
        x = self.pos[0]
        y = self.pos[1]

        self.__draw_box(x, y)
        self.__draw_count(x, y)
        self.__draw_index(x, y)
        self.__draw_pointer()

        if self.node.ground:
            ground = Ground(self.drawer)
            ground.draw(x + self.link[0], y + self.link[1])

        if self.node.link:
            if type(self.node.link) is not int:
                link_cell = Cell(self.drawer, self.node.link, (x, y + self.cell_spacing))
                link_cell.draw()

            if self.node.depth:
                if type(self.node.link) is int:
                    arrow = Arrow(self.drawer)
                    arrow.draw(
                        x + self.link[0], y + self.link[1],
                        x + self.size[0], y - self.cell_spacing * (self.node.depth-1) + self.size[1],
                        self.link[0] * 1.7,
                        ptr_type=3
                    )
                else:
                    arrow = Arrow(self.drawer)
                    arrow.draw(
                        x + self.link[0], y + self.link[1],
                        x + 10, y + self.cell_spacing * self.node.depth,
                        -self.link[0] * 1.7,
                        ptr_type=7
                    )
            elif not self.node.ground:
                arrow = StraightArrow(self.drawer)
                arrow.draw(x + self.link[0], y + self.link[1], x + self.link[0], link_cell.pos[1])
