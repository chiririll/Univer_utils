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

    def __ptr(self, name: str, val=None):
        if val:
            if type(val) is Element:
                self.pointers[name] = val
            elif type(val) is tuple or type(val) is str:
                self.pointers[name] = self.matrix[val]
        else:
            return self.pointers.get(name)

    def __j(self) -> int:
        j = self.__ptr('P0')
        return -1 if j.col == 0 or j.row == 0 else j.col

    def __i(self) -> int:
        i = self.__ptr('Q0')
        return -1 if i.col == 0 or i.row == 0 else i.row

    def run(self):
        self.document.add_step('_task', axial_element=f"m[{self.matrix.pivot[0]}][{self.matrix.pivot[1]}]",
                               task=Document.txt2xml(str(self.matrix) + ','))

        img1 = draw("_practice/img_1", self.matrix)
        self.__ptr('PIVOT', 'PIVOT')
        img2 = draw("_practice/img_2", self.matrix, self.pointers)

        self.document.add_step('_practice', image_1=img1, image_2=img2)

        self.S1()

    def finish(self):
        self.document.add_step('_answer', steps=', '.join(self.steps), matrix=f"{str(self.matrix)}.")
        del self

    def S1(self):
        print("S1: Initialization")
        self.steps.append("S1")

        val = self.matrix['PIVOT'].val
        self.matrix['PIVOT'] = 1.0

        img1 = draw("S1/img_1", self.matrix, self.pointers)

        self.__ptr("P0", self.matrix.base_row[self.matrix.pivot[0]])
        self.__ptr("Q0", self.matrix.base_col[self.matrix.pivot[1]])

        img2 = draw("S1/img_2", self.matrix, self.pointers)

        self.document.add_step('S1', pivot_row=self.matrix.pivot[0], pivot_col=self.matrix.pivot[1], pivot_val=val,
                               res=self.alpha, image_1=img1, image_2=img2)

        self.S2()

    def S2(self):
        print("S2: Handling axial row")
        self.steps.append("S2")

        self.__ptr('P0', self.__ptr('P0').left)
        img1 = draw('S2/img_1', self.matrix, self.pointers)
        j = self.__j()

        if j < 0:
            self.document.add_step('S2_true', P0_col=j, j=j, image_1=img1)
            self.S3()
        else:
            p0_val = self.__ptr('P0').val
            self.__ptr(f'PTR[{j}]', self.matrix.base_col[j])
            self.__ptr('P0').val *= self.alpha

            img2 = draw('S2/img_2', self.matrix, self.pointers)

            self.document.add_step('S2_false', P0_col=self.__ptr('P0').col, P0_val=p0_val, res=self.__ptr('P0').val,
                                   j=j, j0=self.j0, alpha=self.alpha, image_1=img1, image_2=img2)
            self.S2()

    def S3(self):
        print("S3: Finding new row")
        self.steps.append("S3")

        self.__ptr('Q0', self.__ptr('Q0').up)
        img1 = draw('S3/img_1', self.matrix, self.pointers)

        i = self.__i()

        if i < 0:
            self.document.add_step('S3_end', Q0_row=i, i=i, i0=self.i0, image_1=img1)
            self.finish()
        else:
            if i == self.i0:
                self.document.add_step('S3_true', Q0_row=i, i=i, i0=self.i0, image_1=img1)
                self.S3()
            else:
                self.__ptr('P', self.matrix.base_row[i])
                img2 = draw('S3/img_2', self.matrix, self.pointers)

                self.__ptr('P1', self.__ptr('P').left)
                img3 = draw('S3/img_3', self.matrix, self.pointers)

                self.document.add_step('S3_false', Q0_row=i, i=i, i0=self.i0, image_1=img1, image_2=img2, image_3=img3)
                self.S4()

    def S4(self):
        print("S4: Finding new column")
        self.steps.append("S4")

        self.__ptr('P0', self.__ptr('P0').left)
        img1 = draw('S4/img_1', self.matrix, self.pointers)

        j = self.__j()
        if j < 0:
            val = self.__ptr('Q0').val
            self.__ptr('Q0').val = -self.alpha * val
            img2 = draw('S4/img_2', self.matrix, self.pointers)
            self.document.add_step('S4_next', P0_col=j, j=j, j0=self.j0, Q0_val=val, res=self.__ptr('Q0').val, alpha=self.alpha,
                                   image_1=img1, image_2=img2)
            self.S3()
        elif j == self.j0:
            self.document.add_step('S4_true', P0_col=j, j=j, j0=self.j0, image_1=img1)
        else:
            self.document.add_step('S4_false', P0_col=j, j=j, j0=self.j0, image_1=img1)
            self.S5()

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
