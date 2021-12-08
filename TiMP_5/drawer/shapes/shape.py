import math
from svgwrite import Drawing


class Shape:
    def __init__(self, drawer: Drawing, **kwargs):
        self.drawer = drawer

        self.pos = kwargs.pop('pos', (0, 0))
        self.x = self.pos[0]
        self.y = self.pos[1]

        self.__cords = kwargs

    def _get_c(self, name):
        cord = self.__cords.get(name)
        if cord:
            return self.x + cord[0], self.y + cord[1]

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
