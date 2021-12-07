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
