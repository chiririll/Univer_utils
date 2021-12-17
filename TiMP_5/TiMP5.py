from matrix import *
from drawer import draw
from word_parser import Document


class Lab5:
    def __init__(self, matrix: Matrix, name='out'):
        # Document
        self.document = Document(f"output/docs/{name}.doc")

        # Matrix
        self.matrix = matrix
        self.pointers = {}

        # Variables
        self.i = 0
        self.j = 0

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

    def __i(self) -> int:
        i = self.__ptr('Q0')
        self.i = -1 if i.col == 0 or i.row == 0 else i.row
        return self.i

    def __j(self) -> int:
        j = self.__ptr('P0')
        self.j = -1 if j.col == 0 or j.row == 0 else j.col
        return self.j

    def run(self):
        self.document.add_step('_task', axial_element=f"m[{self.matrix.pivot[0]}][{self.matrix.pivot[1]}]",
                               task=Document.txt2xml(str(self.matrix) + ','))

        img1 = draw("_practice/img_1", self.matrix)
        self.__ptr('PIVOT', 'PIVOT')
        img2 = draw("_practice/img_2", self.matrix, self.pointers)

        self.document.add_step('_practice', image_1=img1, image_2=img2)

        self.S1()

    def finish(self):
        self.document.add_step('_answer', steps=', '.join(self.steps), matrix=Document.txt2xml(f"{str(self.matrix)}."))
        self.document.add_step('_conclusion')
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
            self.document.add_step('S4_true', P0_col=j, j=j, j0=self.j0, Q0_val=val, res=self.__ptr('Q0').val, alpha=self.alpha,
                                   image_1=img1, image_2=img2)
            self.S3()
        elif j == self.j0:
            self.document.add_step('S4_repeat', P0_col=j, j=j, j0=self.j0, image_1=img1)
            self.S4()
        else:
            self.document.add_step('S4_false', P0_col=j, j=j, j0=self.j0, image_1=img1)
            self.S5()

    def S5(self):
        print("S5: Finding I,J element")
        self.steps.append("S5")

        col = self.__ptr('P1').col
        if col > self.j:
            self.__ptr('P', self.__ptr('P1'))
            img1 = draw('S5/img_1', self.matrix, self.pointers)
            self.__ptr('P1', self.__ptr('P').left)
            img2 = draw('S5/img_2', self.matrix, self.pointers)

            self.document.add_step('S5_true', P1_col=col, j=self.j, image_1=img1, image_2=img2)

            self.S5()
        elif col == self.j:
            self.document.add_step('S5_false_S7', P1_col=col, j=self.j)
            self.S7()
        else:
            self.document.add_step('S5_false_next', P1_col=col, j=self.j)
            self.S6()

    def S6(self):
        print("S6: Appending I,J element")
        self.steps.append("S6")

        ptr_j_up_row = self.__ptr(f"PTR[{self.j}]").up[0]
        if ptr_j_up_row > self.i:
            self.__ptr(f'PTR[{self.j}]', self.__ptr(f'PTR[{self.j}]').up)
            img1 = draw('S6/img_1', self.matrix, self.pointers)
            self.document.add_step('S6_true', i=self.i, j=self.j, ptr_j_up_row=ptr_j_up_row, image_1=img1)
            self.S6()
        else:
            element = self.matrix.add(Element(0, self.i, self.j, draw_text=False))
            self.__ptr('X', element)
            img1 = draw('S6/img_1', self.matrix, self.pointers)
            element.draw_text = True
            img2 = draw('S6/img_2', self.matrix, self.pointers)
            element.left = self.__ptr('P1').get_cords()
            img3 = draw('S6/img_3', self.matrix, self.pointers)
            element.up = self.__ptr(f"PTR[{self.j}]").up
            img4 = draw('S6/img_4', self.matrix, self.pointers)
            self.__ptr('P').left = element.get_cords()
            img5 = draw('S6/img_5', self.matrix, self.pointers)
            self.__ptr(f"PTR[{self.j}]").up = element.get_cords()
            img6 = draw('S6/img_6', self.matrix, self.pointers)
            self.__ptr('P1', element)
            img7 = draw('S6/img_7', self.matrix, self.pointers)
            self.__ptr(f"PTR[{self.j}]", element)
            img8 = draw('S6/img_8', self.matrix, self.pointers)
            self.document.add_step('S6_false', i=self.i, j=self.j, ptr_j_up_row=ptr_j_up_row,
                                   image_1=img1, image_2=img2, image_3=img3, image_4=img4, image_5=img5, image_6=img6,
                                   image_7=img7, image_8=img8)
            self.S7()

    def S7(self):
        print("S7: Axial operation")
        self.steps.append("S7")

        val_p1 = self.__ptr('P1').val
        self.__ptr('P1').val = val_p1 - self.__ptr('Q0').val * self.__ptr('P0').val
        img1 = draw('S7/img_1', self.matrix, self.pointers)
        if self.__ptr('P1').val == 0:
            self.document.add_step('S7_true', P1_val=val_p1, Q0_val=self.__ptr('Q0').val, P0_val=self.__ptr('P0').val,
                                   res=self.__ptr('P1').val, image_1=img1)
            self.S8()
        else:
            self.__ptr(f"PTR[{self.j}]", self.__ptr('P1'))
            self.__ptr('P', self.__ptr('P1'))
            img2 = draw('S7/img_2', self.matrix, self.pointers)
            self.__ptr('P1', self.__ptr('P').left)
            img3 = draw('S7/img_3', self.matrix, self.pointers)

            self.document.add_step('S7_false', P1_val=val_p1, Q0_val=self.__ptr('Q0').val, P0_val=self.__ptr('P0').val,
                                   res=self.__ptr('P1').val, j=self.j, image_1=img1, image_2=img2, image_3=img3)

            self.S4()

    def S8(self):
        print("S8: Excluding I,J element")
        self.steps.append("S8")

        if self.__ptr(f"PTR[{self.j}]").up != self.__ptr('P1').get_cords():
            self.__ptr(f"PTR[{self.j}]", self.__ptr(f"PTR[{self.j}]").up)
            img1 = draw('S8/img_1', self.matrix, self.pointers)
            self.document.add_step('S8_true', j=self.j, image_1=img1)
            self.S8()
        else:
            self.__ptr(f"PTR[{self.j}]").up = self.__ptr('P1').up
            img1 = draw('S8/img_1', self.matrix, self.pointers)
            self.__ptr('P').left = self.__ptr('P1').left
            img2 = draw('S8/img_2', self.matrix, self.pointers)
            self.matrix.exclude(self.__ptr('P1'))
            self.pointers.pop('P1')
            img3 = draw('S8/img_3', self.matrix, self.pointers)
            self.__ptr('P1', self.__ptr('P').left)
            img4 = draw('S8/img_4', self.matrix, self.pointers)

            self.document.add_step('S8_false', j=self.j,
                                   image_1=img1, image_2=img2, image_3=img3, image_4=img4)
            self.S4()
