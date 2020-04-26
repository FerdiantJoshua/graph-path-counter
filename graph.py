class Graph:
    id = 0
    def __init__(self):
        self.id = Graph.id
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)

    def __str__(self):
        return f'G-{self.id:03d}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__repr__() == other.__repr__()
        elif isinstance(other, str):
            return self.__repr__() == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
