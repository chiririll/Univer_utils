from abc import ABC, abstractmethod
from PIL.ImageDraw import ImageDraw


class Shape(ABC):
    def __init__(self, drawer: ImageDraw, **kwargs):
        self.drawer = drawer

    def draw(self, **kwargs):
        pass
