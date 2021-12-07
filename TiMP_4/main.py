from sort import Sort


def main(task: str):
    sorter = Sort(task)
    sorter.run()


if __name__ == "__main__":
    rels = [
        "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1",     # 21
        "2<3, 2<6, 2<7, 5<1, 4<8, 8<7, 7<9, 1<2, 1<8, 3<7",     # 10
        "2<4, 4<1, 8<7, 6<4, 6<7, 6<8, 3<9, 5<2, 7<4, 9<6",     # 23
        "3<1, 8<5, 9<3, 9<7, 6<2, 2<3, 2<9, 4<8, 1<4, 7<8"      # Test (Zabavnikova)
    ]
    main(rels[2])