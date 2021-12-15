import utils
from matrix import *
from drawer import draw
from word_parser import Document


class Lab5:
    def __init__(self, matrix: Matrix):
        # Document
        self.document = Document("output/docs/out.doc")

        # Matrix
        self.matrix = matrix
        self.pointers = {}

        # Variables
        self.i0 = self.matrix.pivot[0]
        self.j0 = self.matrix.pivot[1]
        self.alpha = 1.0 / self.matrix['PIVOT'].val

        # Answers
        self.steps = []

    def run(self):
        self.document.add_step('_task', axial_element=f"m[{self.matrix.pivot[0]}][{self.matrix.pivot[1]}]",
                               task=Document.txt2xml(str(self.matrix) + ','))

        img1 = draw("_practice/img_1", self.matrix)
        self.pointers["PIVOT"] = self.matrix['PIVOT']
        img2 = draw("_practice/img_2", self.matrix, self.pointers)

        self.document.add_step('_practice', image_1=img1, image_2=img2)

        self.S1()

    def S1(self):
        print("S1: Initialization")
        self.steps.append("S1")

        val = self.matrix['PIVOT'].val
        self.matrix['PIVOT'] = 1.0

        img1 = draw("S1/img_1", self.matrix, self.pointers)

        self.pointers["P0"] = self.matrix[(0, self.matrix.pivot[0])]
        self.pointers["Q0"] = self.matrix[(self.matrix.pivot[1], 0)]

        img2 = draw("S1/img_2", self.matrix, self.pointers)

        self.document.add_step('S1', pivot_row=self.matrix.pivot[0], pivot_col=self.matrix.pivot[1], pivot_val=val,
                               res=self.alpha, image_1=img1, image_2=img2)

        self.S2()

    def S2(self):
        print("S2: Handling axial row")
        self.steps.append("S2")

        self.pointers['P0'] = self.matrix[self.pointers['P0'].left]
        img1 = draw('S2/img_1', self.matrix, self.pointers)
        j = self.pointers['P0']
        j = -1 if j.col == 0 or j.row == 0 else j.col

        if j < 0:
            self.document.add_step('S2_true', P0_col=j, j=j, image_1=img1)
            self.S3()
        else:
            p0_val = self.pointers['P0'].val
            self.pointers['P0'].val *= self.alpha

            img2 = draw('S2/img_2', self.matrix, self.pointers)

            self.document.add_step('S2_false', P0_col=self.pointers['P0'].col, P0_val=p0_val, res=self.pointers['P0'].val,
                                   j=j, alpha=self.alpha, image_1=img1, image_2=img2)
            self.S2()

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
