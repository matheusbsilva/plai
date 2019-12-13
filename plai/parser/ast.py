class AST:
    def __init__(self, token):
        self.token = token
        self.children = []

    def add_child(self, child):
        if not isinstance(child, AST):
            raise TypeError("'%s' must be an instance of AST" % child)

        self.children.append(child)
