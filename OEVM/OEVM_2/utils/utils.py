def get_bin(number: int):
    return f"{number:04b}"


def get_ltr_by_index(index: int):
    return chr(ord('a') + index)


def check_interval(interval, part):
    part = get_bin(part) if type(part) is int else part
    for i, var in enumerate(interval):
        if var == '-':
            continue
        if var != part[i]:
            return '0'
    return '1'
