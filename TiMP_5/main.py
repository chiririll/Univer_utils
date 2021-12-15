from TiMP5 import Lab5

import utils
from matrix import Matrix, Element

matrix = Matrix(
    pivot=(2, 1),
    matrix=[
        Element(50, 1, 1),
        Element(20, 2, 3),
        Element(10, 2, 1),
        Element(5, 4, 4),
        Element(-60, 4, 3),
        Element(-30, 4, 1)
    ]
)


def laba_5():
    laba = Lab5(matrix)
    laba.run()


def test_drawer():
    import drawer
    drawer.draw('test', matrix)


if __name__ == "__main__":
    utils.clear_folder("output/images")

    # test_drawer()
    laba_5()
