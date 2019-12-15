import pytest

from lark import Token

from plai.parser import AST


class TestAST:
    def test_initialization(self):
        ast = AST(Token('TOKEN', 'token'), [])

        assert ast.token == 'token'
        assert ast.children == []

    def test_initialization_with_children(self):
        child = AST(Token('CHILD', 'child'))
        ast = AST(Token('TOKEN', 'token'), [child])

        assert ast.token == 'token'
        assert ast.children == [child]


    def test_add_child_method(self):
        ast = AST(Token('TOKEN', 'token'))
        child = AST(Token('CHILD', 'child'))
        ast.add_child(child)

        assert ast.children[0] == child

    def test_add_child_only_receives_instance_of_AST(self):
        ast = AST(Token('TOKEN', 'token'))

        with pytest.raises(TypeError):
            ast.add_child('child')

    def test_raises_typeerror_for_unvalid_token_type(self):
        with pytest.raises(TypeError):
            AST('token')

    def test_initialization_with_ast(self):
        """
        When initialized with an AST instance it must return that instance
        """

        ast = AST(Token('X', 'x'))

        assert AST(ast) == ast

    def test_print(self):
        root = AST(Token('ROOT', 'root'))
        child1 = AST(Token('CHILD1', 'child1'))
        child2 = AST(Token('CHILD2', 'child2'))

        child1.add_child(child2)
        root.add_child(child1)

        print_result = "root\n child1\n  child2\n"
        assert root.print() == print_result
