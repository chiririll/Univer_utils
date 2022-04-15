import Shared
from Shared.Document.rels import RelType, Image, Xml
from .. import info

from . import threads


class Laba6(Shared.Classes.Laba):

    laba = {
        'type': "Лабораторная работа №6",
        'title': "Оценка рисков информационной безопасности по базовым угрозам в сетевой информационной системе",
        'subject': "OIB",
        'name': "laba6"
    }
    subject = info.OIB

    def __init__(self, task, **params):
        self.task = task

        self.th = []    # Thread type -> PC id -> Thread item
        self.cth = []   # Thread type -> PC id
        self.cthr = []  # PC id
        self.r = []     # PC id
        self.cr = 0

        params['word_params'] = {
            'style': "tstu",
            'parts_folder': "OIB/Laba_6/parts"
        }
        super().__init__(**params)

    def run(self):
        self.title_page()
        self.theory()

        self.part_1()
        self.part_2()
        self.part_3()
        self.part_4()
        self.part_5()

    def title_page(self):
        logo_rel = Image("Shared/src/images/tstu.wmf", "tstu")
        first_footer = Xml(RelType.FOOTER, "footer_first.xml", "Shared/src/parts/footers/first.xml")
        default_footer = Xml(RelType.FOOTER, "footer_default.xml", "Shared/src/parts/footers/default.xml")

        context = {
            'logo_id': self.document.add_relation(logo_rel),
            'first_footer_id': self.document.add_relation(first_footer),
            'default_footer_id': self.document.add_relation(default_footer)
        }
        self.document.add_step('title_pages/tstu', **context)

    def theory(self):
        style = {
            'width': 266,
            'height': 230
        }
        image = Image("OIB/Laba_6/src/image1.emf", style=style)
        image.id = self.document.add_relation(image)

        context = {
            'threads': threads,
            'thread_classes': threads.thread_classes,
            'criticality': self.task,
            'image': image
        }
        self.document.add_step('theory', **context)

    def part_1(self):
        def count_th() -> list:
            th = []
            for thread_type in range(len(threads.threads)):
                thread_type_list = []
                for pc in range(len(threads.threads[thread_type])):
                    pc_list = []
                    for item_val in threads.threads[thread_type][pc]:
                        pc_list.append((item_val / 100) * (self.task[thread_type][pc] / 100))
                    thread_type_list.append(pc_list)
                th.append(thread_type_list)
            return th

        self.th = count_th()

        style = {
            'width': 141,
            'height': 48
        }

        context = {
            'func_1': Image("OIB/Laba_6/src/part_1/func_1.wmf", "p1f1", style),
            'func_2': Image("OIB/Laba_6/src/part_1/func_2.wmf", "p1f2", style),
            'func_3': Image("OIB/Laba_6/src/part_1/func_3.wmf", "p1f3", style),

            'thread_classes': threads.thread_classes,
            'th': self.th
        }

        context['func_1'].id = self.document.add_relation(context['func_1'])
        context['func_2'].id = self.document.add_relation(context['func_2'])
        context['func_3'].id = self.document.add_relation(context['func_3'])

        self.document.add_step('part_1', **context)

    def part_2(self):
        def count_cth() -> list:
            cth = []
            for thread_type in self.th:
                thread_type_list = []
                for pc in thread_type:
                    mult = 1
                    for item in pc:
                        mult *= 1 - item
                    thread_type_list.append(1 - mult)
                cth.append(thread_type_list)
            return cth

        self.cth = count_cth()

        style = {
            'width': 179,
            'height': 48
        }

        context = {
            'func_1': Image("OIB/Laba_6/src/part_2/func_1.wmf", "p2f1", style),
            'func_2': Image("OIB/Laba_6/src/part_2/func_2.wmf", "p2f2", style),
            'func_3': Image("OIB/Laba_6/src/part_2/func_3.wmf", "p2f3", style),

            'thread_classes': threads.thread_classes,
            'cth': self.cth
        }

        context['func_1'].id = self.document.add_relation(context['func_1'])
        context['func_2'].id = self.document.add_relation(context['func_2'])
        context['func_3'].id = self.document.add_relation(context['func_3'])

        self.document.add_step('part_2', **context)

    def part_3(self):
        def count_cthr() -> list:
            cthr = [1] * len(threads.threads[0])
            for thread_type in self.cth:
                for i, pc in enumerate(thread_type):
                    cthr[i] *= 1 - pc
            return list(map(lambda x: 1 - x, cthr))

        self.cthr = count_cthr()

        style = {
            'width': 179,
            'height': 55
        }

        context = {
            'func': Image("OIB/Laba_6/src/part_3/func.wmf", "p3f", style),
            'cthr': self.cthr
        }

        context['func'].id = self.document.add_relation(context['func'])

        self.document.add_step('part_3', **context)

    def part_4(self):
        def count_r() -> list:
            return [cthr * threads.d[i] for i, cthr in enumerate(self.cthr)]

        self.r = count_r()

        style = {
            'width': 103,
            'height': 20
        }

        context = {
            'func': Image("OIB/Laba_6/src/part_4/func.wmf", "p4f", style),
            'r': self.r
        }

        context['func'].id = self.document.add_relation(context['func'])

        self.document.add_step('part_4', **context)

    def part_5(self):
        def count_cr() -> int:
            cr = 1
            for r_i in self.r:
                cr *= 1 - r_i / 100
            return (1 - cr) * 100

        self.cr = count_cr()

        style = {
            'width': 204,
            'height': 60
        }

        context = {
            'func': Image("OIB/Laba_6/src/part_5/func.wmf", "p5f", style),
            'r': self.r,
            'cr': self.cr
        }

        context['func'].id = self.document.add_relation(context['func'])

        self.document.add_step('part_5', **context)
