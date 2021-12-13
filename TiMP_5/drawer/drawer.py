from random import randint

import svgwrite

from . import shapes
from .svg2emf import export_emf
from . import utils


Size = (625, 350)


def draw(filename: str, matrix: dict, pointers: list):
    path = f"output/images/{filename}.svg"
    utils.check_path(path)

    dwg = svgwrite.Drawing(path, Size)

    # Edge elements
    for i in range(1, 5):
        shapes.Cell(dwg, matrix, (i, 0)).draw()
        shapes.Cell(dwg, matrix, (0, i)).draw()

    for cord in matrix.keys():
        shapes.Cell(dwg, matrix, cord).draw()
        # TODO: Draw arrows (links)

    for ptr in pointers:
        shapes.Pointer(dwg, shapes.Cell.get_pos(ptr['cord']), text=ptr['label'], angle=randint(0, 360)).draw()

    dwg.save()

    # Converting to emf
    export_emf(path)

    return {'path': f"output/images/{filename}.emf", 'size': Size}
