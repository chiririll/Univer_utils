from TiMP5 import Lab5

import utils
from matrix import Matrix, Element

example = Matrix(
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
var_11 = Matrix(
    pivot=(3, 4),
    matrix=[
        Element(-40, 2, 4),
        Element(-120, 2, 2),
        Element(30, 2, 1),
        Element(10, 3, 4),
        Element(30, 3, 2),
        Element(-20, 4, 4),
    ]
)
var_1 = Matrix(
    pivot=(4, 4),
    matrix=[
        Element(-40, 1, 4),
        Element(20, 1, 3),
        Element(-30, 1, 2),
        Element(-10, 3, 4),
        Element(40, 4, 4),
        Element(30, 4, 2),
    ]
)


def make_all():
    all = utils.tasks_parser('src/tasks.txt')
    # need = [5, 6, 9, 10, 11, 13, 15, 16, 17, 18, 20, 21, 23, 24]
    need = [9, 11, 13, 16, 17, 21]
    for var in need:
        print(f"\n === Variant {var} ===")
        laba = Lab5(all[var], f"var_{var}")
        laba.run()


def laba_5():
    laba = Lab5(var_11)
    laba.run()


def test_drawer():
    def get_pointers(count: int = 3):
        names = [f"PTR[{i}]" for i in range(count)]
        return dict(zip(names, [example[1, 1]] * count))

    import drawer
    drawer.draw('test', example, get_pointers(4))


if __name__ == "__main__":
    utils.clear_folder("output/images")

    # test_drawer()
    # laba_5()
    make_all()
