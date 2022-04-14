import Shared
from Shared.Document import RelType, Relation
from .. import info


class Laba6(Shared.Classes.Laba):

    laba = {
        'type': "Лабораторная работа №6",
        'title': "Оценка рисков информационной безопасности по базовым угрозам в сетевой информационной системе",
        'subject': "OIB",
        'name': "laba6"
    }
    subject = info.OIB

    def __init__(self, **params):
        params['word_params'] = {
            'style': "tstu"
        }
        super().__init__(**params)

    def run(self):
        self.title_page()

    def title_page(self):
        logo_rel = Relation(RelType.IMAGE, "media/tstu.wmf", "Shared/src/images/tstu.wmf")
        first_footer = Relation(RelType.FOOTER, "footer_first.xml", "Shared/src/parts/footers/first.xml")
        default_footer = Relation(RelType.FOOTER, "footer_default.xml", "Shared/src/parts/footers/default.xml")

        context = {
            'logo_id': self.document.add_relation(logo_rel),
            'first_footer_id': self.document.add_relation(first_footer),
            'default_footer_id': self.document.add_relation(default_footer)
        }
        self.document.add_step('title_pages/default', **context)
