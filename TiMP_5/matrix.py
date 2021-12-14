class Element:
    def __init__(self, val, row, col, left: tuple = None, up: tuple = None):
        self.left = left
        self.up = up

        self.row = row
        self.col = col
        self.val = val

    def get_cords(self) -> tuple:
        return self.row, self.col

    def find_links(self, cords: tuple, matrix: dict):
        self.left = (cords[0], 0)
        self.up = (0, cords[1])

        for i in range(cords[0] - 1, 0, -1):
            if (i, cords[1]) in matrix.keys():
                self.left = (i, cords[1])
                break
        for i in range(cords[1] - 1, 0, -1):
            if (cords[0], i) in matrix.keys():
                self.left = (cords[0], i)
                break


class Matrix:
    def __init__(self, pivot, matrix):
        self.__matrix = {}
        self.base_row = [Element(None, i, 0) for i in range(1, 5)]
        self.base_col = [Element(None, 0, i) for i in range(1, 5)]

        # Converting matrix
        if type(matrix) is dict:
            self.__matrix = matrix
        elif type(matrix) is list:
            self.__matrix = self.list_to_dict(matrix)

        self.pivot = pivot
        self.ptr = []

        # Updating links
        self.__update_links()

    def __str__(self) -> str:
        """ Returns matrix as string (task string) """
        task_string = ""
        row = 1
        for el in self.__matrix.values():
            while el.row > row:
                row += 1
                task_string += '\n'
            task_string += f"m[{el.row}][{el.col}] = {el.val}, "
        return task_string[:-2]

    def __getitem__(self, item) -> Element:
        """ Return element of matrix by cords or name (PIVOT) """
        if type(item) is tuple:
            return self.__matrix[item]

        match item:
            case 'PIVOT':
                return self.__matrix[self.pivot]

    def __iter__(self) -> Element:
        for el in self.__matrix.values():
            yield el

    def __update_links(self) -> None:
        """ Update up and left fields in every element """
        # def find_next(cords, d: int):
        #     """
        #
        #     :param cords:
        #     :param d:
        #     :return:
        #     """
        #     for n in range(cords[d]-1, -1, -1):
        #         new = [n, n]
        #         new[d] = cords[d]
        #         if self.__matrix.get(new) or n == 0:
        #             return new

        # Left
        for base in self.base_row:
            col = 4
            while not self.__matrix.get((base.row, col)) and col > 0:
                col -= 1

            el = (base.row, col)
            self.base_row[base.row - 1].left = el
            for col in range(col, -1, -1):
                left = (base.row, col)
                if left != el and (self.__matrix.get(left) or col == 0):
                    self.__matrix[el].left = left
                    el = left
        # Up
        for base in self.base_col:
            row = 4
            while not self.__matrix.get((row, base.col)) and row > 0:
                row -= 1

            el = (row, base.col)
            self.base_col[base.col - 1].up = el
            for row in range(row, -1, -1):
                up = (row, base.col)
                if up != el and (self.__matrix.get(up) or row == 0):
                    self.__matrix[el].up = up
                    el = up

    def add(self, element: Element) -> None:
        """ Appends element to matrix """
        self.__matrix[element.get_cords()] = element
        self.__update_links()

    @staticmethod
    def list_to_dict(matrix: list) -> dict:
        matrix_dict = {}
        for el in matrix:
            matrix_dict[el.get_cords()] = el
        return matrix_dict
