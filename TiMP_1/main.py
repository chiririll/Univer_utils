from TiMP1 import Laba1


def main():
    task_15 = [
        [1, 1, 13],
        [1, 4, 6],
        [1, 4, 11],
        [1, 4, 6],
        [1, 4, 10]
    ]
    task_test = [
        [0, 2, 2],      # TOP
        [0, 4, 3],
        [1, 1, 10]      # BOTTOM
    ]

    laba = Laba1(task_test)
    laba.run()


if __name__ == "__main__":
    main()
