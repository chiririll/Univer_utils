from PIL import Image, ImageFont, ImageDraw

from TiMP.TiMP_3 import utils
from . import shapes


width = 700
height = 120


def draw(nodes: list, path: str):
    depth = utils.calc_max_depth(nodes)
    size = (width, height + shapes.Cell.cell_spacing * depth)

    img = Image.new("RGB", size, "#ffffff")
    drawer = ImageDraw.ImageDraw(img)

    font = ImageFont.truetype("/timesi.ttf", 14)

    # Text
    drawer.text((65, 30), "k", "#000000", font)
    drawer.text((10, 48), "COUNT[k]", "#000000", font)
    drawer.text((14, 66), "QLINK[k]", "#000000", font)
    drawer.text((31, 84), "TOP[k]", "#000000", font)

    for i in range(depth):
        drawer.text((45, 53 + shapes.Cell.cell_spacing * (i + 1)), "SUC", "#000000", font)
        drawer.text((40, 73 + shapes.Cell.cell_spacing * (i + 1)), "NEXT", "#000000", font)

    for node in nodes:
        cell = shapes.Cell(drawer, node, (60 * node.k + 110, 50))
        cell.draw()

    img.save(path)
    return {'path': path, 'size': size, 'depth': depth}
