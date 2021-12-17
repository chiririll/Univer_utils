import os

from matrix import Element, Matrix


def tasks_parser(filename: str) -> dict:
    def var_parser(lines: list):
        # Variant number
        var = int(lines[0].split()[1])

        # Matrix
        elements = []
        for line in lines[2:6]:
            for el in line.split():
                parts = el[1:].replace(']', ' ').replace('[', ' ').split('=')
                cords = tuple(map(int, parts[0].split()))
                val = float(parts[1])
                elements.append(Element(val, *cords))

        # Pivot
        pivot = tuple(map(int, lines[6][16:].replace(']', ' ').replace('[', ' ').split()[:-1]))

        return var, Matrix(pivot=pivot, matrix=elements)

    f = open(filename, 'r', encoding='UTF-8')
    tasks = {}

    lines = f.readlines()
    for i in range(0, len(lines), 9):
        res = var_parser(lines[i:i+9])
        tasks[res[0]] = res[1]
    return tasks


def clear_folder(path: str):
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isdir(f):
            clear_folder(f)
        else:
            os.remove(f)
