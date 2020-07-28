import pytest

from lark.exceptions import UnexpectedToken
from lark import Token
from plai.parser import parse
from plai.symbol import Symbol
from plai.parser.ast import AST
from .factory_ast import number_node, string_node, name_node
from .factory_ast import attr_call_node, assign_node, op_node, binop_node


class TestBasicTokens:
    def test_token_number(self):
        assert parse('7') == number_node(7)
        assert parse('8.1') == number_node(8.1)

    def test_token_string(self):
        assert parse('"hello"') == string_node('"hello"')
        assert parse('"hello world"') == string_node('"hello world"')

    def test_escaped_token_string(self):
        assert parse(r'"hello \"world\""') == string_node(r'"hello \"world\""')
        assert parse(r'"hello \n world"') == string_node(r'"hello \n world"')
        assert parse(r'"hello \t world"') == string_node(r'"hello \t world"')

    def test_variable_call(self):
        assert parse('bar') == name_node("bar")

    def test_attribute_call(self):
        assert parse('bar.foo') == attr_call_node('bar', 'foo')


class TestBasicExp:
    def test_sum(self):
        assert parse('1 + 2') == binop_node('+', 1, 2)

    def test_subtraction(self):
        assert parse('1 - 2') == binop_node('-', 1, 2)

    def test_multiplication(self):
        assert parse('1 * 2') == binop_node('*', 1, 2)

    def test_division(self):
        assert parse('1 / 2') == binop_node('/', 1, 2)

    def test_precedence_of_mult_expr(self):
        root = op_node('+')
        op = binop_node('*', 2, 5)
        root.add_child(op)
        root.add_child(AST(Token('NUMBER', 2)))

        assert parse('2 * 5 + 2') == root

    def test_expression_with_parentheses(self):
        op = binop_node('+', 2, 4)
        assert parse('(2 + 4)') == op

    def test_precedence_using_parentheses(self):
        root = op_node('*')
        root.add_child(binop_node('+', 2, 5))
        root.add_child(number_node(3))
        assert parse('(2 + 5) * 3') == root

    def test_expression_with_variables(self):
        root = op_node('+')
        child = op_node('+')
        child.add_child(name_node('foo'))
        child.add_child(name_node('bar'))
        root.add_child(child)
        root.add_child(number_node(2))

        assert parse('foo + bar + 2') == root

    def test_sum_using_functions(self):
        root = op_node('+')
        func = name_node('foo')
        root.add_child(func)
        root.add_child(number_node(1))

        assert parse('foo() + 1') == root

    def test_sum_using_strings(self):
        root = op_node('+')
        root.add_child(string_node('"hello"'))
        root.add_child(string_node('"world"'))
        assert parse('"hello" + "world"') == root

    def test_sum_using_attr_call(self):
        root = op_node('+')
        root.add_child(attr_call_node('foo', 'bar'))
        root.add_child(attr_call_node('fuzz', 'buzz'))

        assert parse('foo.bar + fuzz.buzz') == root


class TestFunctionCall:
    def test_basic_function_call(self):
        assert parse('foo()') == name_node('foo')

    def test_function_call_exp_as_argument(self):
        root = name_node('foo')
        root.add_child(binop_node('+', 1, 2))
        root.add_child(binop_node('*', 8, 5))

        assert parse('foo(1+2, 8*5)') == root

    def test_function_call_passing_string_as_argument(self):
        root = name_node('foo')
        root.add_child(string_node('"bar"'))
        assert parse('foo("bar")') == root

    def test_function_call_variable_as_argument(self):
        root = name_node('foo')
        root.add_child(name_node('bar'))
        assert parse('foo(bar)') == root

    def test_funcion_call_attr_call_as_argument(self):
        root = name_node('foo')
        root.add_child(attr_call_node('bar', 'fuzz'))
        assert parse('foo(bar.fuzz)') == root

    def test_function_call_function_as_argument(self):
        root = name_node('foo')
        root.add_child(name_node('bar'))
        assert parse('foo(bar())') == root

    def test_function_call_mixed_arguments(self):
        root = name_node('foo')
        root.add_child(number_node(1))
        root.add_child(binop_node('+', 1, 2))
        root.add_child(name_node('x'))
        root.add_child(attr_call_node('fuzz', 'buzz'))

        assert parse('foo(1, 1+2, x, fuzz.buzz)') == root


class TestAssignment:
    def test_assignment_number(self):
        root = assign_node()
        root.add_child(name_node('foo'))
        root.add_child(number_node(1))

        assert parse('foo = 1') == root

    def test_assignment_expr(self):
        root = assign_node()
        root.add_child(name_node('bar'))
        root.add_child(binop_node('+', 1, 2))
        assert parse('bar = 1 + 2') == root

    def test_assign_comp_expr(self):
        op = op_node('*')
        op.add_child(binop_node('+', 1, 2))
        op.add_child(number_node(5))

        root = assign_node()
        root.add_child(name_node('bar'))
        root.add_child(op)
        assert parse('bar = (1 + 2) * 5') == root

    def test_assignment_function(self):
        root = assign_node()
        root.add_child(name_node('bar'))
        func = name_node('foo')
        func.add_child(number_node(1))
        root.add_child(func)

        assert parse('bar = foo(1)') == root


@pytest.mark.skip("Not refactoring this now to finish simpler interpretations")
class TestPipeline:
    def test_pipeline_declaration(self):
        assert parse('pipeline(bar): {foo()}') == [Symbol.PIPELINE,
                                                 [Symbol('bar')],
                                                 [Symbol('foo')]]
        assert parse('pipeline(bar, fuzz): {foo()}') == [Symbol.PIPELINE,
                                                       [Symbol('bar'),
                                                           Symbol('fuzz')],
                                                       [Symbol('foo')]]

    def test_sugar_column_call(self):
        assert parse('.col') == [Symbol.COLUMN, 'col']
        assert parse('."col"') == [Symbol.COLUMN, 'col']

    def test_invalid_sugar_column_call(self):
        assert parse('.1') != [Symbol.COLUMN, 1]

        with pytest.raises(UnexpectedToken):
            parse('.()')

    def test_multiple_stmts_on_pipeline(self):
        parsed = parse('pipeline(bar): {foo(.bar) fuzz(.bar)}')
        assert parsed == [Symbol.PIPELINE, [Symbol('bar')], [Symbol('foo'), [Symbol.COLUMN, 'bar']], [Symbol('fuzz'), [Symbol.COLUMN, 'bar']]]
