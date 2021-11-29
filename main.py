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

    max_depth = 0
    ptr = None
    for rel_id, rel in enumerate(rels):
        print(f"Relation #{rel_id} ({rel[0]} < {rel[1]})")

        document.add_step('T2', j=str(rel[0]), k=str(rel[1]))

        # Creating folder
        path = f"output/rel_{rel_id}"
        utils.mkdir(path)

        # Finding bottom node
        parent = nodes[rel[0]]
        tmp = False
        while parent.link is not None:
            parent = parent.link
            tmp = True

        # Incrementing count
        nodes[rel[1]].count += 1
        img0 = drawer.draw(nodes, f"{path}/0.png")
        if ptr:
            ptr.ptr = False

        # Adding node
        parent.link = Node(ptr=True, id=rel[1], tmp=tmp)
        ptr = parent.link
        img1 = drawer.draw(nodes, f"{path}/1.png")

        # Displaying suc field
        parent.link.count = rel[1]
        img2 = drawer.draw(nodes, f"{path}/2.png")

        # Checking complex node
        if tmp:
            parent.link.link = -1
            img3 = drawer.draw(nodes, f"{path}/3.png")

            nodes[rel[0]].depth = img3['depth']
            img4 = drawer.draw(nodes, f"{path}/4.png")

            nodes[rel[0]].depth = None

            # Swapping nodes
            t = nodes[rel[0]].link
            nodes[rel[0]].link = parent.link
            nodes[rel[0]].link.link = t
            parent.link = None
            parent.ground = True
        else:
            parent.link.ground = True
            img3 = drawer.draw(nodes, f"{path}/3.png")

            parent.ground = False
            img4 = drawer.draw(nodes, f"{path}/4.png")

            # parent.link.ptr = False

        params = {
            'j': str(rel[0]), 'k': str(rel[1]),
            'count_k': str(nodes[rel[1]].count - 1), 'count_k_inc': str(nodes[rel[1]].count),
            'image_0': img0,
            'image_1': img1,
            'image_2': img2,
            'image_3': img3,
            'image_4': img4,
        }

        if img4['depth'] > max_depth or rel_id < 2:
            document.add_step('T3', **params)
            max_depth = img4['depth']
        else:
            document.add_step('T3_min', **params)

    document.add_step('T2_null')
    document.save()


if __name__ == "__main__":
    rels = [
        "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1",     # 21
        "2<3, 2<6, 2<7, 5<1, 4<8, 8<7, 7<9, 1<2, 1<8, 3<7",     # 10
        "2<4, 4<1, 8<7, 6<4, 6<7, 6<8, 3<9, 5<2, 7<4, 9<6",     # 23
        "1<4, 1<7, 5<2, 9<1, 9<6, 4<5, 4<7, 8<6, 6<2, 2<3"      # Test
    ]
    main(rels[2])
