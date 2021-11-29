import drawer
import utils
from node import Node
from word_parser import Document


def main(rels: str):
    # Cleaning folder
    utils.clear_folder("output")
    # Creating folder
    utils.mkdir("output/_start")
    # Copying doc file
    utils.copy_file("src/empty_doc/Empty.doc", "output/Output.doc")

    document = Document("output/Output.doc")
    rels = utils.parse_rels(rels)

    nodes = []
    for i in range(10):
        nodes.append(Node(k=i))

    img0 = drawer.draw(nodes, "output/_start/0.png")

    for node in nodes:
        node.count = 0
        node.ground = True

    img1 = drawer.draw(nodes, "output/_start/1.png")

    document.add_step('T1', image_0=img0, image_1=img1)

    for rel_id, rel in enumerate(rels):
        print(f"Relation #{rel_id} ({rel[0]}, {rel[1]})")
        document.add_step('T2', j=str(rel[0]), k=str(rel[1]))
        # Creating folder
        path = f"output/rel_{rel_id}"
        utils.mkdir(path)

        parent = nodes[rel[0]]
        tmp = False
        while parent.link is not None:
            parent = parent.link
            tmp = True

        nodes[rel[1]].count += 1
        img0 = drawer.draw(nodes, f"{path}/0.png")

        parent.link = Node(ptr=True, id=rel[1], tmp=tmp)
        img1 = drawer.draw(nodes, f"{path}/1.png")

        parent.link.count = rel[1]
        img2 = drawer.draw(nodes, f"{path}/2.png")

        if tmp:
            parent.link.ptr = False
            # TODO: Draw arrows

            # Swapping nodes
            t = nodes[rel[0]].link
            nodes[rel[0]].link = parent.link
            nodes[rel[0]].link.link = t
            parent.link = None
            img3 = drawer.draw(nodes, f"{path}/3.png")
            parent.ground = True
            img4 = drawer.draw(nodes, f"{path}/4.png")
        else:
            parent.link.ground = True
            img3 = drawer.draw(nodes, f"{path}/3.png")

            parent.ground = False
            img4 = drawer.draw(nodes, f"{path}/4.png")

            parent.link.ptr = False

        document.add_step(
            'T3',
            j=str(rel[0]), k=str(rel[1]),
            image_0=img0,
            image_1=img1,
            image_2=img2,
            image_3=img3,
            image_4=img4,
        )

    document.save()


if __name__ == "__main__":
    rels = [
        "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1",     # 21
        "2<3, 2<6, 2<7, 5<1, 4<8, 8<7, 7<9, 1<2, 1<8, 3<7",     # 10
        "2<4, 4<1, 8<7, 6<4, 6<7, 6<8, 3<9, 5<2, 7<4, 9<6",     # 23
        "1<4, 1<7, 5<2, 9<1, 9<6, 4<5, 4<7, 8<6, 6<2, 2<3"      # Test
    ]
    main(rels[2])
