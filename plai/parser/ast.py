from lark import Token

from plai.symbol import Symbol


class AST:
    def __new__(cls, token, children=[]):
        if isinstance(token, AST):
            new = token
        else:
            if not isinstance(token, (Token, Symbol, AST)):
                raise TypeError("'%s' must be an instance of Token or Symbol")

            new = super().__new__(cls)
            new.token = token
            new.children = []

        [new.add_child(child) for child in children]

        return new

    def add_child(self, child):
        if not isinstance(child, AST):
            raise TypeError("'%s' must be an instance of AST" % child)

        self.children.append(child)

    def __str__(self):
        return str(self.token)

    def print(self, level=0):
        rep = level*" " + self.__str__() + "\n"
        for node in self.children:
            rep += node.print(level+1)

        return rep
