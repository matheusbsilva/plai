import pytest
from plai.parser import AST


class TestAST:
    def test_initialization(self):
        ast = AST('token')

        assert ast.token == 'token'
        assert ast.children == []

    def test_add_child_method(self):
        ast = AST('token')
        child = AST('child')
        ast.add_child(child)

        assert ast.children[0] == child

    def test_add_child_only_receives_instance_of_AST(self):
        ast = AST('token')

        with pytest.raises(TypeError):
            ast.add_child('child')
