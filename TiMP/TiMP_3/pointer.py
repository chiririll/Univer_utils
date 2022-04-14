class Pointer:
    def __init__(self, node=None):
        self.node = node

    def move(self, node):
        self.hide()
        self.node = node
        self.show()

    def show(self):
        if self.node:
            self.node.ptr = True

    def hide(self):
        if self.node:
            self.node.ptr = False

    def get_suc(self):
        if self.node:
            return self.node.count
        return 0

    def is_empty(self):
        return self.node is None

    def next(self):
        self.hide()
        self.node = self.node.link
        self.show()
