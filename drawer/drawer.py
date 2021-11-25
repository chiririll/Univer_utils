from PIL import Image
from PIL.ImageDraw import ImageDraw

from . import shapes


size = (1000, 500)


def draw(nodes: list, path: str):
    img = Image.new("RGB", size, "#ffffff")
    drawer = ImageDraw(img)

    # TODO: add text

    for node in nodes:
        cell = shapes.Cell(drawer, node, (60 * node.k + 200, 50))
        cell.draw()

    img.save(path)
