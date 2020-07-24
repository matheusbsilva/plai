from lark import Token


class AST:
    def __init__(self, token):
        if isinstance(token, Token):
            self.token = token
        else:
            raise TypeError("'%s' must be an isntance of Token" % token)
        self.children = []

    def __str__(self):
        return str(self.token)

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.token == other.token and \
                    self.children == other.children:
                return True

            return False

        return NotImplemented

    def __repr__(self):
        rep = "%s" % self.token
        if self.children:
            rep += "["
            for child in self.children:
                rep += "%s " % repr(child)
            rep += "]"

        return rep

    def add_child(self, child):
        if not isinstance(child, AST):
            raise TypeError("'%s' must be an instance of AST" % child)

        self.children.append(child)

    def print(self, level=0):
        rep = level*" " + self.__str__() + "\n"
        for node in self.children:
            rep += node.print(level+1)

        return rep

