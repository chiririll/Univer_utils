from collections import deque

import utils
from drawer import drawer
from node import Node
from pointer import Pointer
from word_parser import Document


class Sort:
    def __init__(self, task):
        # Pre run tasks
        self.clear_folder()

        # Containers
        self.document = Document("output/Output.doc")
        self.rels = utils.parse_rels(task)
        self.nodes = [Node(k=i) for i in range(10)]

        # Variables
        self.p = Pointer()
        self.n = 9

        # Queue
        # self.queue = deque()
        self.f = 0
        self.r = 0

        # Answer
        self.steps = []
        self.answer = []

        # Params
        self.max_depth = 0

    def __get_queue(self):
        q = self.f
        queue = []
        while q is not None:
            queue.append(q)
            for i in range(self.nodes[q].count - 1):
                queue.append(q)
            q = self.nodes[q].qlink if q is not self.r else None
        return ' → '.join(list(map(str, queue)))

    def clear_folder(self):
        # Cleaning folders
        utils.clear_folder("output")
        # Creating folders
        utils.mkdir("output/images/_start")
        utils.mkdir("output/images/_P2/")

    def run(self):
        # Preparing
        self.T1()

        # Registering relations
        for rel_id, rel in enumerate(self.rels):
            path = f"output/images/rel_{rel_id}"
            utils.mkdir(path)
            # Executing steps
            self.T2(rel)
            self.T3(rel_id, rel, path)
        self.T2()

        # Starting sort
        self.T4()

    def T1(self):
        print("T1.\t Preparing")
        img0 = drawer.draw(self.nodes, "output/images/_start/0.png")

        for i in range(1, 10):
            self.nodes[i].count = 0
            self.nodes[i].ground = True

        img1 = drawer.draw(self.nodes, "output/images/_start/1.png")

        self.document.add_step('T1', image_0=img0, image_1=img1)

    def T2(self, rel=None):
        if rel:
            self.document.add_step('T2', j=str(rel[0]), k=str(rel[1]))
            print(f"T2.\t Next relation ({rel[0]} < {rel[1]})")
        else:
            self.document.add_step('T2_null')
            print(f"T2.\t Next relation (Empty)")

    def T3(self, rel_id, rel, path):
        print(f"T3.\t Registering relation #{rel_id} ({rel[0]} < {rel[1]})")
        # Finding bottom node
        parent = self.nodes[rel[0]]
        while parent.link is not None:
            parent = parent.link

        # Incrementing count
        self.nodes[rel[1]].count += 1
        img0 = drawer.draw(self.nodes, f"{path}/0.png")
        self.p.hide()

        # Adding node
        parent.link = Node(ptr=True, id=rel[1])
        self.p.move(parent.link)
        img1 = drawer.draw(self.nodes, f"{path}/1.png")

        # Displaying suc field
        parent.link.count = rel[1]
        img2 = drawer.draw(self.nodes, f"{path}/2.png")

        # Checking complex node
        if parent is not self.nodes[rel[0]]:
            parent.link.link = -1
            parent.link.depth = utils.calc_depth(self.nodes[rel[0]])
            img3 = drawer.draw(self.nodes, f"{path}/3.png")

            self.nodes[rel[0]].depth = utils.calc_depth(self.nodes[rel[0]])
            img4 = drawer.draw(self.nodes, f"{path}/4.png")

            self.nodes[rel[0]].depth = None
            parent.link.depth = None

            # Swapping nodes
            t = self.nodes[rel[0]].link
            self.nodes[rel[0]].link = parent.link
            self.nodes[rel[0]].link.link = t
            parent.link = None
            parent.ground = True
        else:
            parent.link.ground = True
            img3 = drawer.draw(self.nodes, f"{path}/3.png")

            parent.ground = False
            img4 = drawer.draw(self.nodes, f"{path}/4.png")

        params = {
            'j': rel[0], 'k': rel[1],
            'count_k': self.nodes[rel[1]].count - 1, 'count_k_inc': self.nodes[rel[1]].count
        }

        if img4['depth'] > self.max_depth or rel_id < 2:
            self.document.add_step('T3', **params, image_0=img0, image_1=img1, image_2=img2, image_3=img3, image_4=img4)
            self.max_depth = img4['depth']
        else:
            self.document.add_step('T3_min', **params, image_4=img4)

    def T4(self):
        print("T4.\t Looking for zeroes")
        self.steps.append('T4')

        self.document.add_step('T4')

        self.r = 0
        self.nodes[0].qlink = 0

        for k in range(1, 10):
            step = 'T4_true' if self.nodes[k].count == 0 else 'T4_false'
            self.document.add_step(step, k=k, R=self.r, count_k=self.nodes[k].count)
            if self.nodes[k].count == 0:
                self.nodes[self.r].qlink = k
                self.r = k

        self.f = self.nodes[0].qlink

        img = drawer.draw(self.nodes, "output/images/_P2/T4.png")
        self.document.add_step('T4_final', image=img, qlink_0=self.nodes[0].qlink, queue=self.__get_queue())

        self.T5()

    def T5(self):
        print("T5.\t Adding to answer")
        self.steps.append('T5')

        self.answer.append(self.f)
        if self.f == 0:
            self.document.add_step('T5_true', F=self.f)
            self.T8()
            return

        self.n -= 1                             # N--
        self.p.move(self.nodes[self.f].link)    # P <- TOP[F]

        img = drawer.draw(self.nodes, "output/images/_P2/T5.png")
        self.document.add_step('T5_false', F=self.f, N=self.n + 1, N_dec=self.n, image=img)

        self.T6()

    def T6(self):
        print("T6.\t Erasing relation")
        self.steps.append('T6')

        if self.p.is_empty():
            self.document.add_step('T6_true')
            self.T7()
            return

        params = {
            'suc_p': self.p.get_suc(),
            'count_suc_p': self.nodes[self.p.get_suc()].count,
            'count_suc_p_dec': self.nodes[self.p.get_suc()].count - 1,
            'R': self.r,
        }

        self.nodes[self.p.get_suc()].count -= 1             # COUNT[SUC(P)] -= 1

        if self.nodes[self.p.get_suc()].count == 0:
            self.nodes[self.r].qlink = self.p.get_suc()     # QLINK[R] <- SUC(P)
            self.r = self.p.get_suc()                       # R <- SUC(P)

        self.nodes[self.r].qlink = self.p.get_suc()         # QLINK[R] <- SUC(P)
        self.r = self.p.get_suc()                           # R <- SUC(P)

        self.p.next()                                       # P <- NEXT(P)

        img = drawer.draw(self.nodes, "output/images/_P2/T6.png")
        self.document.add_step('T6_false', **params, image=img, queue=self.__get_queue())
        self.T6()

    def T7(self):
        print("T7.\t Excluding from queue")
        self.steps.append('T7')

        # if len(self.queue) == 0:
        #     self.queue.append(0)

        f = self.f
        if self.nodes[f].count == 0:
            self.f = self.nodes[self.f].qlink   # F <- QLINK[F]
        self.document.add_step('T7', queue=self.__get_queue(), F=f, qlink_F=self.nodes[f].qlink)
        self.T5()

    def T8(self):
        print("T8.\t Finishing process")
        self.steps.append('T8')

        self.document.add_step('T8', answer_set=', '.join(list(map(str, self.answer))), answer_sequence=', '.join(self.steps))
