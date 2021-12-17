import svgwrite

from . import shapes
from . import utils
from .svg2emf import export_emf


Size = (625, 350)


def draw(filename: str, matrix, pointers: dict = None):
    ptrs = {}
    if pointers is not None:
        for name, element in pointers.items():
            if element.get_cords() in ptrs:
                ptrs[element.get_cords()].append(name)
            else:
                ptrs[element.get_cords()] = [name]

    path = f"output/images/{filename}.svg"
    utils.check_path(path)

    dwg = svgwrite.Drawing(path, Size)

    # Base elements
    for base in [*matrix.base_row[1:], *matrix.base_col[1:]]:
        shapes.Cell(dwg, matrix, base, ptrs.get(base.get_cords())).draw()

    # Elements
    for el in matrix:
        shapes.Cell(dwg, matrix, el, ptrs.get(el.get_cords())).draw()

    dwg.save()

    # Converting to emf
    export_emf(path)

    return {'path': f"output/images/{filename}.emf", 'size': Size}
