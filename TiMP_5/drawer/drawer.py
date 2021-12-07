import svgwrite

import shapes
from TiMP_5 import utils, word_parser


def draw(filename: str, matrix: dict, pointers: list):
    path = f"output/images/{filename}.svg"
    utils.check_path(path)

    dwg = svgwrite.Drawing(path, (1000, 500))

    # Edge elements
    for i in range(1, 5):
        shapes.Cell(dwg, matrix, (i, 0)).draw()
        shapes.Cell(dwg, matrix, (0, i)).draw()

    for cord in matrix.keys():
        shapes.Cell(dwg, matrix, cord).draw()

    dwg.save()

    # Converting to emf
    word_parser.export_emf(path)


if __name__ == "__main__":
    matrix = {
        (1, 1): 50,
        (2, 3): 20,
        (2, 1): 10,
        (4, 4): 5,
        (4, 3): -60,
        (4, 1): -30
    }
    draw("test", matrix, [])
