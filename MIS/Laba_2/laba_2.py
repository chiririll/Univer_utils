import Shared.Classes
from Shared.Document.rels import RelType, Image, Xml
from .. import info


class Laba2(Shared.Classes.Laba):
    laba = {
        'type': "Лабораторная работа №2",
        'title': "Оценка рисков информационной безопасности по базовым угрозам в сетевой информационной системе",
        'subject': "MIS",
        'name': "laba2"
    }
    subject = info.MIS

    def __init__(self, **params):
        super().__init__(**params)

    def run(self):
        self.title_page()

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
