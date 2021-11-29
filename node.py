class Node:
    def __init__(self, **kwargs):
        self.k = kwargs.get('k', None)
        self.id = kwargs.get('id', self.k or 0)
        self.count = kwargs.get('count', None)
        self.link = kwargs.get('link', None)

        self.ptr = kwargs.get('ptr', False)
        self.ground = kwargs.get('ground', False)
        self.tmp = kwargs.get('tmp', False)
        self.depth = kwargs.get('depth', None)
