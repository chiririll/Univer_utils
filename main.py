import os

import drawer
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


def main(rels: str):
    rels = parse_rels(rels)

    # Cleaning folder
    clear_folder("output")
    # Creating folder
    mkdir("output/_start")

    nodes = []
    for i in range(10):
        nodes.append(Node(k=i))

    drawer.draw(nodes, "output/_start/0.png")

    for node in nodes:
        node.count = 0
        node.ground = True

    drawer.draw(nodes, "output/_start/1.png")

    for rel_id, rel in enumerate(rels):
        print(f"Relation #{rel_id} ({rel[0]}, {rel[1]})")
        # Creating folder
        path = f"output/rel_{rel_id}"
        mkdir(path)

        parent = nodes[rel[0]]
        tmp = False
        while parent.link is not None:
            parent = parent.link
            tmp = True

        nodes[rel[1]].count += 1
        parent.link = Node(ptr=True, id=rel[1], tmp=tmp)
        drawer.draw(nodes, f"{path}/0.png")

        parent.link.count = rel[1]
        drawer.draw(nodes, f"{path}/1.png")

        if tmp:
            parent.link.ptr = False
            # Swapping nodes
            t = nodes[rel[0]].link
            nodes[rel[0]].link = parent.link
            nodes[rel[0]].link.link = t
            parent.link = None
            parent.ground = True
            drawer.draw(nodes, f"{path}/2.png")
        else:
            parent.link.ground = True
            drawer.draw(nodes, f"{path}/2.png")

            parent.ground = False
            drawer.draw(nodes, f"{path}/3.png")

            parent.link.ptr = False


if __name__ == "__main__":
    rels = [
        "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1",     # 21
        "2<3, 2<6, 2<7, 5<1, 4<8, 8<7, 7<9, 1<2, 1<8, 3<7",     # 10
        "2<4, 4<1, 8<7, 6<4, 6<7, 6<8, 3<9, 5<2, 7<4, 9<6",     # 23
        "1<4, 1<7, 5<2, 9<1, 9<6, 4<5, 4<7, 8<6, 6<2, 2<3"      # Test
    ]
    main(rels[2])
