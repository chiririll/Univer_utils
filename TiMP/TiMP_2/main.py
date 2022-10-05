from TiMP2 import Laba2


def main():
    task_test = {
        'BASE': [-1, 2, 5, 9],
        'TOP': [1, 2, 8, 11],
        'SEQUENCE': "I2I3I3"
    }

    task_5 = {
        'BASE': [-1, 3, 9, 13],
        'TOP': [1, 6, 11, 14],
        'SEQUENCE': "I4I3I3I2I4I4I1I4I4I4"
    }

    laba = Laba2(task_5, var=5)
    laba.run()


if __name__ == "__main__":
    main()
