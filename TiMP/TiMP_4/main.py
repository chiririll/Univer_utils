from TiMP4 import Laba4


def main():
    test = [
        [(1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (0, -1, 0, 0)],
        [(1, 2, 0, 0), (-2, 0, 1, 0), (-1, 0, 0, 1), (0, -1, 0, 0)]
    ]

    var_7 = [
        [(3, 1, 1, 0), (-3, 0, 0, 1), (-2, 0, 0, 0), (0, -1, 0, 0)],
        [(-2, 0, 1, 0), (3, 0, 0, 1), (-1, 0, 0, 0), (0, -1, 0, 0)]
    ]

    var_8 = [
        [(1, 1, 1, 0), (-3, 1, 0, 1), (1, 0, 0, 0), (0, -1, 0, 0)],
        [(-1, 1, 1, 0), (-2, 1, 0, 1), (2, 0, 0, 1), (0, -1, 0, 0)],
    ]

    var_15 = [
        [(3, 1, 1, 1), (-2, 1, 1, 0), (-3, 0, 0, 1), (0, -1, 0, 0)],
        [(4, 1, 1, 1), (2, 1, 1, 0), (-1, 1, 0, 0), (0, -1, 0, 0)]
    ]

    Laba4(test, filename="test", var=0, name="test").run()


if __name__ == "__main__":
    main()
