from PIL import ImageFont

from .shape import Shape
from .pointer import Pointer
from .ground import Ground
from .arrow import Arrow


class Cell(Shape):
    size = (30, 60)
    width = 1
    color = "#000000"

    k_pos = (10, -20)
    count_pos = (10, 5)
    font_size = 14

    link = (15, 45)

    def __init__(self, drawer, node, pos):
        super().__init__(drawer)

        self.node = node
        self.pos = pos
        self.font = ImageFont.truetype("src/timesnewroman.ttf", self.font_size)

    def __draw_box(self, x, y):
        self.drawer.line((x, y, x, y + self.size[1]), self.color, self.width)
        self.drawer.line((x + self.size[0], y, x + self.size[0], y + self.size[1]), self.color, self.width)

        self.drawer.line((x, y + self.size[1] // 2, x + self.size[0], y + self.size[1] // 2), self.color, self.width)

        self.drawer.line((x, y, x + self.size[0], y), self.color, self.width)
        self.drawer.line((x, y + self.size[1], x + self.size[0], y + self.size[1]), self.color, self.width)

    def __draw_count(self, x, y):
        if self.node.count is not None:
            self.drawer.text((x + self.count_pos[0], y + self.count_pos[1]), str(self.node.count), self.color, self.font)

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

        for i, link_node in enumerate(self.node.links):
            link_cell = Cell(self.drawer, link_node, (x, y + 110*(i+1)))
            link_cell.draw()

            if not self.node.ground:
                arrow = Arrow(self.drawer)
                shift = 5*i + 20 if i > 0 else 0
                arrow.draw(x + self.link[0], y + self.link[1], x + self.link[0], link_cell.pos[1], shift)
