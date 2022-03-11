from TiMP2 import Laba2


def main():
    task_test = {
        'BASE': [-1, 2, 5, 9],
        'TOP': [1, 2, 8, 11],
        'SEQUENCE': "I2I3I3"
    }
    task_test_1 = {
        'BASE': [-1, 3, 9, 9],
        'TOP': [0, 6, 9, 10],
        'SEQUENCE': "I1I4I4I1I4I2I4I4I1I1"
    }

    laba = Laba2(task_test)
    laba.run()


if __name__ == "__main__":
    main()
