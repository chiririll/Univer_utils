import os

import drawer
from node import Node

task = "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1"


def topologic_sort():

    pass


def parse_rels(s: str):
    rels = []
    for t in task.replace(' ', '').split(','):
        parts = t.split('<')
        rels.append((int(parts[0]), int(parts[1])))
    return rels


def main():
    rels = parse_rels(task)
    #rels = [(5, 4)]

    nodes = []
    for i in range(10):
        nodes.append(Node(k=i))

    drawer.draw(nodes, "output/start/0.png")

    for node in nodes:
        node.count = 0
        node.ground = True

    drawer.draw(nodes, "output/start/1.png")

    for rel_id, rel in enumerate(rels):
        # Creating folder
        path = f"output/rel_{rel_id}"
        if not os.path.isdir(path):
            os.makedirs(path)

        nodes[rel[1]].count += 1
        link_id = nodes[rel[0]].add_link(Node(ptr=True))
        drawer.draw(nodes, f"{path}/0.png")

        nodes[rel[0]].links[link_id].count = rel[1]
        drawer.draw(nodes, f"{path}/1.png")

        nodes[rel[0]].links[link_id].ground = True
        drawer.draw(nodes, f"{path}/2.png")

        nodes[rel[0]].ground = False
        drawer.draw(nodes, f"{path}/3.png")

        nodes[rel[0]].links[link_id].ptr = False


if __name__ == "__main__":
    main()
