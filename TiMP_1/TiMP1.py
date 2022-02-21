from word_parser import Document


class Laba1:
    def __init__(self, task: list = None, filename="out", var=0, name="Ivanov I.I."):
        # Document
        self.document = Document(f"output/{filename}.doc")

        # Data
        self.task = task
        self.var = var
        self.name = name

    def run(self):
        self.document.add_step('_title_page')
        self.document.add_step('1_1_PROG_START')
        self.document.add_step('1_2_PROG_CARD')
        self.document.add_step('1_3_PROG_END')

        self.document.add_step('2_1_RESULT_START')
        self.document.add_step('2_2_RESULT_CARD')
        self.document.add_step('2_3_RESULT_END')

        self.document.add_step('3_1_PROTOCOL')
        self.document.add_step('1_2_PROG_CARD')
        self.document.add_step('3_3_PROTOCOL_STEP', cards=self.document.get_step_xml('3_4_PROTOCOL_CARD'))