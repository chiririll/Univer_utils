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
        image = Image("OIB/Laba_6/src/image1.png", style=style)
        image.id = self.document.add_relation(image)

        context = {
            'threads': threads,
            'thread_classes': thread_classes,
            'criticality': self.task,
            'image': image
        }
        self.document.add_step('theory', **context)

    def step_1(self):
        pass

