from PIL import Image, ImageFont, ImageDraw

from node import Node
from . import shapes


width = 700
height = 150
height_delta = 100


def calc_depth(nodes: list):
    max = 0
    for node in nodes:
        cur = 0
        while type(node.link) is Node:
            node = node.link
            cur += 1
        if cur > max:
            max = cur
    return max


def draw(nodes: list, path: str):
    depth = calc_depth(nodes)
    size = (width, height + height_delta * depth)

    img = Image.new("RGB", size, "#ffffff")
    drawer = ImageDraw.ImageDraw(img)

    font = ImageFont.truetype("src/timesnewroman.ttf", 14)

    # Text
    drawer.text((65, 30), "k", "#000000", font)
    drawer.text((10, 55), "COUNT[k]", "#000000", font)
    drawer.text((14, 75), "QLINK[k]", "#000000", font)
    drawer.text((31, 95), "TOP[k]", "#000000", font)

    for i in range(depth):
        drawer.text((45, 158 + 100*i), "SUC", "#000000", font)
        drawer.text((40, 187 + 100*i), "NEXT", "#000000", font)

    for node in nodes:
        cell = shapes.Cell(drawer, node, (60 * node.k + 110, 50))
        cell.draw()

    img.save(path)
    return {'path': path, 'size': size, 'depth': depth}
