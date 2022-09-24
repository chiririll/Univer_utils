import Shared.Classes
from Shared.Document.rels import RelType, Image, Xml

from .. import info


class Laba2(Shared.Classes.Laba):
    laba = {
        'type': "Лабораторная работа №2",
        'title': "Преобразование яркости изображений",
        'subject': "Izobrazhenia",
        'name': "laba2"
    }

    subject = info.Izobr

    def __init__(self, image, **params):

        self.image = image

        params['word_params'] = {
            'style': "tstu",
            'parts_folder': "Izobrazhenia/Laba_2/parts"
        }

        super().__init__(**params)

    def run(self):
        self.title_page()
        self.beginning()

        self.step_1()
        self.step_2()
        self.step_3()
        self.step_4()
        self.step_5()
        self.step_6()

    def step_1(self):
        self.document.add_step('steps/1')

    def step_2(self):
        self.document.add_step('steps/2')

    def step_3(self):
        self.document.add_step('steps/3')

    def step_4(self):
        self.document.add_step('steps/4')

    def step_5(self):
        self.document.add_step('steps/5')

    def step_6(self):
        self.document.add_step('steps/6')

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

    def beginning(self):
        self.document.add_step('objective')
        self.document.add_step('tasks')
        self.document.add_step('begin')
