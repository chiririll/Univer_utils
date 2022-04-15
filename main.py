import OIB
from TiMP import TiMP_1


def OIS():
    # Criticality
    var11 = [
        # Server, PC-1, PC-2, PC-3
        [69, 4, 14, 14],    # Privacy
        [74, 16, 21, 12],   # Integrity
        [53, 12, 15, 12]    # Availability
    ]

    laba = OIB.Laba6(var11)
    laba.run()


def TiMP1():
    TiMP_1.main()


if __name__ == "__main__":
    OIS()
