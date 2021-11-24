class Node:
    def __init__(self, **kwargs):
        self.k = kwargs.get('k', None)
        self.count = kwargs.get('count', None)
        self.links = kwargs.get('links', [])

        self.ptr = kwargs.get('ptr', False)
        self.ground = kwargs.get('ground', False)

    def add_link(self, link):
        self.links.append(link)
        return len(self.links) - 1
