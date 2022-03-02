from TiMP_2.word_parser import Document


class Laba2:

    def __init__(self, task: list, filename="out", var=0, name="Ivanov I.I."):
        # Document
        self.document = Document(f"output/{filename}.doc")

        # Task

        # Data
        self.var = var
        self.name = name

    def run(self):
        self.document.add_step("_title_page", var=self.var, name=self.name)
        self.document.add_step("_task")

        self.document.add_step('practice')

        self.document.add_step("init/memory")
        self.document.add_step("memory")
        self.document.br()

        self.document.add_step("init/oldtop")

        self.document.add_step("_conclusion")
