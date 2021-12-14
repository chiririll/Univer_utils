import svgwrite

from . import shapes
from . import utils
from .svg2emf import export_emf

Size = (625, 350)


def draw(filename: str, matrix, pointers: dict = None):
    if pointers is None:
        pointers = {}
    path = f"output/images/{filename}.svg"
    utils.check_path(path)

    dwg = svgwrite.Drawing(path, Size)

    # Base elements
    for base in [*matrix.base_row, *matrix.base_col]:
        shapes.Cell(dwg, matrix, base).draw()

    # Elements
    for el in matrix:
        shapes.Cell(dwg, matrix, el, pointers.get(el.get_cords())).draw()

    dwg.save()

    # Converting to emf
    export_emf(path)

    return {'path': f"output/images/{filename}.emf", 'size': Size}
