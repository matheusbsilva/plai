import pytest

from lark import Token

from plai.parser import AST


class TestAST:
    def test_initialization(self):
        token = Token('TOKEN', 'token')
        ast = AST(token)

        assert ast.token == token
        assert ast.children == []

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

    def test_print(self):
        root = AST(Token('ROOT', 'root'))
        child1 = AST(Token('CHILD1', 'child1'))
        child2 = AST(Token('CHILD2', 'child2'))

        child1.add_child(child2)
        root.add_child(child1)

        print_result = "root\n child1\n  child2\n"
        assert root.print() == print_result

    def test_compare_ast_with_no_ast(self):
        ast = AST(Token('ROOT', 'root'))

        assert (ast == 'foo') is False

    def test_compare_asts(self):
        ast_r = AST(Token('ROOT', 'root'))
        child_r = AST(Token('CHILD', 'child'))
        ast_r.add_child(child_r)

        ast_f = AST(Token('FOO', 'foo'))

        assert not ast_r == ast_f
        assert ast_r == ast_r


