from TiMP_2.word_parser import Document


class Laba2:

    def __init__(self, task: list, filename="out", var=0, name="Ivanov I.I."):
        # Document
        self.document = Document(f"output/{filename}.doc")

        # Task

        # Data
        self.var = var
        self.name = name

    def test(self):
        self.document.add_step("append/start")
        self.document.add_step("append/step")
        self.document.add_step("append/step_false")
        self.document.add_step("append/step_true")
        self.document.add_step("append/end")

    def run(self):
        self.test()
        return

        self.document.add_step("_title_page", var=self.var, name=self.name)
        self.document.add_step("_task")

        self.document.add_step('practice')

        self.document.add_step("init/memory")
        self.document.add_step("memory")
        self.document.br()

        self.document.add_step("init/oldtop")

        self.document.add_step("_conclusion")
