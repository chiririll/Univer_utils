import os


def parse_rels(s: str):
    rels = []
    for t in s.replace(' ', '').split(','):
        parts = t.split('<')
        rels.append((int(parts[0]), int(parts[1])))
    return rels


def mkdir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path)


def clear_folder(path: str):
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isdir(f):
            clear_folder(f)
        else:
            os.remove(f)


def copy_file(src: str, dst: str):
    f_src = open(src, 'rb')
    f_dst = open(dst, 'wb')

    f_dst.write(f_src.read())

    f_dst.close()
    f_src.close()
