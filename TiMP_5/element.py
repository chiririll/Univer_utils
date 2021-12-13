class Element:
    def __init__(self, val, left: tuple = None, up: tuple = None):
        self.val = val

        self.left = left
        self.up = up

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
