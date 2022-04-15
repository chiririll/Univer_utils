import Shared
from Shared.Document.rels import RelType, Image, Xml
from .. import info

from .threads import thread_classes, threads


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
        params['word_params'] = {
            'style': "tstu",
            'parts_folder': "OIB/Laba_6/parts"
        }
        super().__init__(**params)

    def run(self):
        self.title_page()
        self.theory()

        self.part_1()

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
            'thread_classes': thread_classes,
            'criticality': self.task,
            'image': image
        }
        self.document.add_step('theory', **context)

    def part_1(self):
        style = {
            'width': 141,
            'height': 48
        }

        context = {
            'func_1': Image("OIB/Laba_6/src/part_1/func_1.wmf", style=style),
            'func_2': Image("OIB/Laba_6/src/part_1/func_2.wmf", style=style),
            'func_3': Image("OIB/Laba_6/src/part_1/func_3.wmf", style=style),

            'threads': threads,
            'thread_classes': thread_classes,
            'criticality': self.task
        }

        context['func_1'].id = self.document.add_relation(context['func_1'])
        context['func_2'].id = self.document.add_relation(context['func_2'])
        context['func_3'].id = self.document.add_relation(context['func_3'])

        self.document.add_step('part_1', **context)

