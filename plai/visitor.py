class ASTVisitor:
    def __init__(self, env):
        self._env = env

    def visit(self, node):
        method_name = 'visit_%s' % node.token.type
        visitor_method = getattr(self, method_name, self.generic_visit)

        return visitor_method(node)

    def generic_visit(self, node):
        raise ValueError('Cannot evaluate node of type %s' % node.token.type)

    def visit_NUMBER(self, node):
        return float(node.token.value)

    def visit_NAME(self, node):
        try:
            value = self._env[node.token.value]
            return value
        except KeyError:
            raise NameError('name %s is not defined' % node.token.value)

    def visit_STRING(self, node):
        return node.token.value[1:-1].replace('\\"', "")\
                .replace('\\n', '\n')\
                .replace('\\t', '\t')

    def visit_PLUS(self, node):
        # TODO: change this kind of node to BINOP implementation
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])

        return left + right

    def visit_MINUS(self, node):
        # TODO: change this kind of node to BINOP implementation
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])

        return left - right

