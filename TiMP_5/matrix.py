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
            if item[0] == 0:
                return self.base_row[item[1]]
            if item[1] == 0:
                return self.base_col[item[0]]
            return self.__matrix[item]

        match item:
            case 'PIVOT':
                return self.__matrix[self.pivot]

    def __iter__(self) -> Element:
        for el in self.__matrix.values():
            yield el

    def __update_links(self) -> None:
        """ Update up and left fields in every element """
        def find_next(cords: tuple, d: int):
            """
            Function for finding next left (d = 0) or up (d = 1) element
            :param cords: start cords
            :param d: index of changing cord (0 for col (left), 1 for row (up))
            :return: cords of the next element
            """
            for n in range(cords[(d+1) % 2]-1, -1, -1):
                new = (n, cords[1]) if d else (cords[0], n)
                if n == 0 or self.__matrix.get(new):
                    return new

        # Left
        for base in self.base_row:
            base.left = find_next((base.row, 5), 0)

            new = base.left
            while not (new[0] == 0 or new[1] == 0):
                el = find_next(new, 0)
                self.__matrix[new].left = el
                new = el

        # Up
        for base in self.base_col:
            base.up = find_next((5, base.col), 1)

            new = base.up
            while not (new[0] == 0 or new[1] == 0):
                el = find_next(new, 1)
                self.__matrix[new].up = el
                new = el

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
