import random

from .TiMP1 import Laba1


def generate_rand(count: int):
    return [[0, random.randint(1, 4), random.randint(1, 13)] for i in range(count)]


def main():
    task_test = [
        [0, 2, 2],  # TOP
        [0, 4, 3],
        [1, 1, 10]  # BOTTOM
    ]

    laba = Laba1(generate_rand(9))
    laba.run()


if __name__ == "__main__":
    main()
