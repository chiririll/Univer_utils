import svgwrite

# from . import shapes
# from . import utils
# from .svg2emf import export_emf

import shapes
import utils
from svg2emf import export_emf

padding = (50, 50)
spacing = (30, 100)


def draw(filename: str, pols, pointers: dict = None):
    def calculate_size():
        parts_count = []
        for p in pols:
            parts_count.append(len(p))

        return 2 * padding[0] + max(parts_count) * 5 * shapes.Part.w + (max(parts_count) - 1) * spacing[0], \
               2 * padding[1] + len(pols) * shapes.Part.h + (len(pols) - 1) * spacing[1]

    if pointers is None:
        pointers = {}

    path = f"output/images/{filename}.svg"
    utils.check_path(path)

    dwg = svgwrite.Drawing(path, calculate_size())

    # Drawing cells
    for i, pol in enumerate(pols):
        for j, part in enumerate(pol):
            pos = (
                padding[0] + shapes.Part.w * 5 * j + spacing[0] * j,
                padding[1] + shapes.Part.h * i + spacing[1] * i
            )
            p = shapes.Part(dwg, pos, part, [])
            p.draw()

            if len(part) < 5 or part[4] is None:
                continue    # Empty links

            arrow_pos = p.get_arrow()
            if part[4] > j:
                # Straight arrow
                shift = 0 if part[4] == j+1 else shapes.Part.h
                shapes.StraightArrow(
                    dwg, arrow_pos,
                    (pos[0] + 5 * shapes.Part.w * (part[4] - j) + spacing[0] * (part[4] - j), arrow_pos[1]),
                    shift
                ).draw()
            else:
                # Reverse arrow
                shapes.Arrow(dwg, arrow_pos, (padding[0], arrow_pos[1]), 180, 2 * shapes.Part.h).draw()

    dwg.save()

    # Converting to emf
    export_emf(path)

    return {'path': f"output/images/{filename}.emf", 'size': calculate_size()}


if __name__ == "__main__":
    test = [[[1, 1, 0, 0, 1], [1, 0, 1, 0, 2], [1, 0, 0, 1, 3], [0, -1, 0, 0, 0]],
            [[1, 2, 0, 0, 1], [2, 0, 1, 0, 2], [-1, 0, 0, 1, 3], [0, -1, 0, 0, 0]]]

    draw("test", test)
