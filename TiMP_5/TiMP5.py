import utils
from drawer import draw
from word_parser import Document


class Lab5:
    def __init__(self, task):
        task = utils.parse_task(task)

        # Document
        self.document = Document("output/docs/out.doc")

        # Matrix
        self.matrix = task['matrix']
        self.pivot = task['pivot']

        # Variables
        self.pointers = []

        # Answers
        self.steps = []

    def run(self):
        self.S1()

    def S1(self):
        print("S1: Initialization")
        self.steps.append("S1")

        img1 = draw("S1_1", self.matrix, [])
        img2 = draw("S2_2", self.matrix, [{'label': "PIVOT", 'cord': (2, 1)}])

        val = self.matrix[self.pivot]
        self.document.add_step('S1', pivot_row=self.pivot[0], pivot_col=self.pivot[1], pivot_val=val,
                               res=1.0/val, image_1=img1, image_2=img2)

    def S2(self):
        print("S2: Handling axial row")
        self.steps.append("S2")

        pass

    def S3(self):
        print("S3: Finding new row")
        self.steps.append("S3")

        pass

    def S4(self):
        print("S4: Finding new column")
        self.steps.append("S4")

        pass

    def S5(self):
        print("S5: Finding I,J element")
        self.steps.append("S5")

        pass

    def S6(self):
        print("S6: Appending I,J element")
        self.steps.append("S6")

        pass

    def S7(self):
        print("S7: Axial operation")
        self.steps.append("S7")

        pass

    def S8(self):
        print("S8: Excluding I,J element")
        self.steps.append("S8")

        pass
