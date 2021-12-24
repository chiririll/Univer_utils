import math
from svgwrite import Drawing


class Shape:

    text_style = "font-size:%ipt; font-family:%s" % (12, "Times New Roman")

    color = "#000000"
    width = 2

    def __init__(self, drawer: Drawing, **kwargs):
        self.drawer = drawer

        self.pos = kwargs.pop('pos', (0, 0))
        self.x = self.pos[0]
        self.y = self.pos[1]

        self.__cords = kwargs

    def get_c(self, name, x=None, y=None, pos=None):
        if pos:
            x, y = pos
        elif x is None or y is None:
            x, y = self.x, self.y

        cord = None
        if type(name) is str:
            cord = self.__cords.get(name)
        elif type(name) is tuple:
            cord = name

        return x + cord[0], y + cord[1] if cord else None

    def draw(self):
        pass

    # Useful methods
    @staticmethod
    def get_angle(line1: tuple, line2: tuple):
        a = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
        b = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])

        try:
            return math.degrees(math.acos((a[0] * b[0] + a[1] * b[1]) /
                                          (math.sqrt(a[0] * a[0] + a[1] * a[1]) * math.sqrt(b[0] * b[0] + b[1] * b[1]))))
        except ValueError:
            return 0

    @staticmethod
    def get_distance(src: tuple, dst: tuple) -> float:
        x1, y1 = src
        x2, y2 = dst
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
