import os


def clear_folder(path: str):
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isdir(f):
            clear_folder(f)
        else:
            os.remove(f)


def generate_pol(pol: list) -> list:
    res = []
    for i, part in enumerate(pol):
        if part[0] == 0:
            continue
        valid = abs(part[0]) != 1

        if i > 0:
            res.append((" - " if part[0] < 0 else " + ") + (str(abs(part[0])) if abs(part[0]) != 1 else ""))
        elif abs(part[0]) != 1:
            res.append(str(part[0]))
        elif part[0] < 0:
            res.append('-')

        variables = ['x', 'y', 'z']
        for i in range(1, 4):
            if part[i] != 0:
                valid = True
                res.append(variables[i - 1])
                res.append('^' + (str(part[i]) if part[i] != 1 else ""))

        if not valid:
            res.append("1")
    return res


def generate_xml(equation: list) -> str:
    res = "<w:r><w:t xml:space=\"preserve\">"
    for p in equation:
        if p[0] == '^':
            res += "</w:t></w:r>"
            res += "<w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t xml:space=\"preserve\">"
            res += p[1:]
            res += "</w:t></w:r><w:r><w:t xml:space=\"preserve\">"
        else:
            res += p
    res += "</w:t></w:r>"
    return res
