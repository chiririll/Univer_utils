from svgwrite import Drawing


class Shape:
    def __init__(self, drawer: Drawing, **kwargs):
        self.drawer = drawer

    def draw(self):
        pass
