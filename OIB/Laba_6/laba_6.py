import Shared


class Laba6(Shared.Classes.Laba):

    info = {
        'subject': "OIB",
        'name': "laba6"
    }

    def __init__(self, **params):
        super().__init__(**params)

    def run(self):
        self.document.add_paragraph(f"My variant is {self.executor.variant}, I was made by {self.executor}.")

