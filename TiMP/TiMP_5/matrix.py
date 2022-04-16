class Element:
    def __init__(self, val, row, col, left: tuple = None, up: tuple = None, draw_text=True):
        self.draw_text = draw_text
        self.is_pivot = False

        self.left = left
        self.up = up

        self.row = row
        self.col = col
        self.val = int(val) if type(val) is float and int(val) == val else val

    def __setattr__(self, key, value):
        match key:
            case 'val':
                if not self.__dict__['is_pivot'] and type(value) is float and int(value) == value:
                    self.__dict__['val'] = int(value)
                else:
                    self.__dict__['val'] = value
            case _:
                self.__dict__[key] = value

    def get_cords(self) -> tuple:
        return self.row, self.col


class Matrix:
    def __init__(self, pivot, matrix):
        self.__matrix = {}

        self.base_row = []
        self.base_row.append(None)
        self.base_row += [Element(None, i, 0) for i in range(1, 5)]

        self.base_col = []
        self.base_col.append(None)
        self.base_col += [Element(None, 0, i) for i in range(1, 5)]

        # Converting matrix
        if type(matrix) is dict:
            self.__matrix = matrix
        elif type(matrix) is list:
            self.__matrix = self.list_to_dict(matrix)

        self.pivot = pivot

        # Named elements
        self.__names = {
            'PIVOT': self.pivot
        }

        # Updating links
        self.__update_links()
        self.__matrix[self.pivot].is_pivot = True

    def __str__(self) -> str:
        """ Returns matrix as string (task string) """
        # Converting to 2d array
        matrix = [[None for i in range(len(self.base_col) - 1)] for i in range(len(self.base_row) - 1)]
        for cord, el in self.__matrix.items():
            matrix[cord[0]-1][cord[1]-1] = el.val

        task_string = ""
        for i in range(len(matrix)):
            for j in range(len(matrix[i])-1, -1, -1):
                if matrix[i][j] is not None:
                    task_string += f"m[{i+1}][{j+1}] = {matrix[i][j]}, "
            task_string += '\n'
        return task_string[:-3]

    def __getitem__(self, i, j=None):
        """ Return element of matrix by cords or name (PIVOT) """
        if type(i) is tuple:
            if i[0] == 0:
                return self.base_col[i[1]] if 0 < i[1] < len(self.base_col) else None
            if i[1] == 0:
                return self.base_row[i[0]] if 0 < i[0] < len(self.base_row) else None
            return self.__matrix.get(i)
        elif type(i) is int:
            return self.__matrix.get((i, j))
        elif type(i) is str:
            return self.__matrix.get(self.__names.get(i))
        else:
            return None

    def __setitem__(self, key, value):
        if type(value) is Element:
            self[key] = value
        else:
            self[key].val = value

    def __iter__(self) -> Element:
        for el in self.__matrix.values():
            yield el

    def __update_links(self) -> None:
        """ Update up and left fields in every element """
        # Left
        for base in self.base_row[1:]:
            base.left = self.find_next((base.row, 5), 0)

            new = base.left
            while not (new[0] == 0 or new[1] == 0):
                el = self.find_next(new, 0)
                self.__matrix[new].left = el
                new = el

        # Up
        for base in self.base_col[1:]:
            base.up = self.find_next((5, base.col), 1)

            new = base.up
            while not (new[0] == 0 or new[1] == 0):
                el = self.find_next(new, 1)
                self.__matrix[new].up = el
                new = el

    def find_next(self, cords: tuple, d: int):
        """
        Function for finding next left (d = 0) or up (d = 1) element
        :param cords: start cords
        :param d: index of changing cord (0 for col (left), 1 for row (up))
        :return: cords of the next element
        """
        for n in range(cords[(d + 1) % 2] - 1, -1, -1):
            new = (n, cords[1]) if d else (cords[0], n)
            if n == 0 or self.__matrix.get(new):
                return new

    def add(self, element: Element):
        """ Appends element to matrix """
        self.__matrix[element.get_cords()] = element
        return self.__matrix[element.get_cords()]

    def exclude(self, element) -> None:
        """ Excluding element from matrix """
        if type(element) is tuple:
            self.__matrix.pop(element)
        elif type(element) is Element:
            self.__matrix.pop(element.get_cords())

    @staticmethod
    def list_to_dict(matrix: list) -> dict:
        matrix_dict = {}
        for el in matrix:
            matrix_dict[el.get_cords()] = el
        return matrix_dict
