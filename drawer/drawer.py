from PIL import Image
from PIL.ImageDraw import ImageDraw

from . import shapes


size = (1000, 500)
relations = "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1"


def draw(nodes: list, path: str):
    img = Image.new("RGB", size, "#ffffff")
    drawer = ImageDraw(img)

    for node in nodes:
        cell = shapes.Cell(drawer, node, (60 * node.k + 200, 50))
        cell.draw()

    img.save(path)
