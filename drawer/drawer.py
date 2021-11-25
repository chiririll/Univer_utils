from PIL import Image, ImageFont, ImageDraw

from . import shapes


size = (700, 450)


def draw(nodes: list, path: str):
    img = Image.new("RGB", size, "#ffffff")
    drawer = ImageDraw.ImageDraw(img)

    font = ImageFont.truetype("src/timesnewroman.ttf", 14)

    # Text
    drawer.text((65, 30), "k", "#000000", font)
    drawer.text((10, 55), "COUNT[k]", "#000000", font)
    drawer.text((14, 75), "QLINK[k]", "#000000", font)
    drawer.text((31, 95), "TOP[k]", "#000000", font)

    for i in range(3):
        drawer.text((45, 158 + 100*i), "SUC", "#000000", font)
        drawer.text((40, 187 + 100*i), "NEXT", "#000000", font)



    for node in nodes:
        cell = shapes.Cell(drawer, node, (60 * node.k + 110, 50))
        cell.draw()

    img.save(path)
