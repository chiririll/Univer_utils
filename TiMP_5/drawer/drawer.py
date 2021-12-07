import svgwrite

import shapes


def draw(path: str, matrix: dict, pointers: list):

    dwg = svgwrite.Drawing(path)

    # Edge elements
    for i in range(1, 5):
        shapes.Cell(dwg, matrix, (i, 0)).draw()
        shapes.Cell(dwg, matrix, (0, i)).draw()

    for cord in matrix.keys():
        shapes.Cell(dwg, matrix, cord).draw()

    # TODO

    dwg.save()


if __name__ == "__main__":
    matrix = {
        (1, 1): 50,
        (2, 3): 20,
        (2, 1): 10,
        (4, 4): 5,
        (4, 3): -60,
        (4, 1): -30
    }
    draw("../output/test.svg", matrix, [])
