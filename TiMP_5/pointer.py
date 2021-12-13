class Pointer:
    def __init__(self, name: str, pos: tuple, matrix: dict):
        self.pos = pos
        self.__matrix = matrix

        self.name = name

        self.row = pos[0]
        self.col = pos[1]

        self.val = matrix[pos]
