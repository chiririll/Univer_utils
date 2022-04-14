import Shared


class Laba6(Shared.Classes.Laba):

    def _info(self):
        self.laba['subject'] = "OIB"
        self.laba['name'] = "laba6"

    def run(self):
        print(f"My variant is {self.executor.variant}, I made by {self.executor}.")

    def _get_info(self):
        return "OIB", "laba6"
