import pytest

from plai.visitor import ASTVisitor
from plai.environment import env
from .factory_ast import number_node, generic_node, name_node
from .factory_ast import string_node, binop_node


class TestASTVisitor:
    def setup(self):
        self.e = env()
        self.visitor = ASTVisitor(self.e)

    def test_visitor_instance_has_env(self):

        assert self.visitor._env == self.e

    def test_visit_unknow_type_fall_on_generic_visit(self):
        with pytest.raises(ValueError):
            self.visitor.visit(generic_node('FOO', 'bar'))

    def test_visit_NUMBER_node(self):
        node = number_node(7)

        assert self.visitor.visit(node) == 7

    def test_visit_NAME_not_assigned(self):
        node = name_node('foo')
        with pytest.raises(NameError):
            self.visitor.visit(node)

    def test_visit_NAME_node(self):
        self.e['bar'] = 1
        node = name_node('bar')

        assert self.visitor.visit(node) == 1

    def test_visit_STRING_node(self):
        node_default = string_node('"hello world"')
        node_special_n = string_node('"hello \n world"')
        node_special_t = string_node('"hello \t world"')
        node_escape = string_node('"hello \"world\""')

        assert self.visitor.visit(node_default) == 'hello world'
        assert self.visitor.visit(node_special_n) == 'hello \n world'
        assert self.visitor.visit(node_special_t) == 'hello \t world'
        assert self.visitor.visit(node_escape) == 'hello "world"'

    def test_visit_PLUS_node(self):
        node = binop_node('+', '1', '6')

        assert self.visitor.visit(node) == 7

    def test_visit_MINUS_node(self):
        node = binop_node('-', '1', '6')

        assert self.visitor.visit(node) == -5

