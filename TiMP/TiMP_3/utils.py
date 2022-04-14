import os

from node import Node


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


def calc_max_depth(nodes: list) -> int:
    max = 0
    for node in nodes:
        cur = calc_depth(node)
        if cur > max:
            max = cur
    return max


def calc_depth(node: Node) -> int:
    depth = 0
    while type(node.link) is Node:
        node = node.link
        depth += 1
    return depth
