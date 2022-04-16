from sort import Sort


Variants = {
    8:  "6<5, 6<9, 1<4, 4<8, 8<7, 9<7, 9<8, 2<1, 2<6, 3<2",
    9:  "1<5, 1<9, 5<2, 6<5, 3<4, 3<8, 2<7, 9<3, 9<7, 4<2",
    11: "7<1, 7<4, 7<5, 1<6, 9<3, 5<1, 2<8, 8<7, 3<1, 3<6",
    10: "2<3, 2<6, 2<7, 5<1, 4<8, 8<7, 7<9, 1<2, 1<8, 3<7",
    15: "7<5, 4<6, 1<8, 1<9, 8<7, 8<9, 6<5, 5<2, 3<1, 3<7",
    21: "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1",
    22: "1<8, 9<2, 6<3, 6<7, 2<1, 3<1, 5<2, 5<3, 5<4, 7<5",
    23: "2<4, 4<1, 8<7, 6<4, 6<7, 6<8, 3<9, 5<2, 7<4, 9<6",
    24: "5<2, 6<1, 6<2, 2<1, 8<9, 9<7, 3<5, 3<6, 7<4, 7<6"
}


def main():
    variant = 0
    name = "test"

    sorter = Sort(Variants[variant], var=variant, name=name)
    sorter.run()


if __name__ == "__main__":
    main()
