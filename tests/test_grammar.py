from plai.parser import parse
from plai.symbol import Symbol


class TestBasicTokens:
    def test_token_number(self):
        assert parse('7') == 7
        assert parse('8.1') == 8.1

    def test_token_string(self):
        assert parse('"hello"') == "hello"
        assert parse('"hello world"') == "hello world"

    def test_escaped_token_string(self):
        assert parse(r'"hello \"world\""') == 'hello "world"'
        assert parse(r'"hello \n world"') == "hello \n world"
        assert parse(r'"hello \t world"') == "hello \t world"

    def test_variable_call(self):
        assert parse('bar') == Symbol('bar')


class TestBasicExp:
    def test_sum(self):
        assert parse('1 + 2') == [Symbol("+"), 1, 2]

    def test_subtraction(self):
        assert parse('1 - 2') == [Symbol('-'), 1, 2]

    def test_multiplication(self):
        assert parse('1 * 2') == [Symbol('*'), 1, 2]

    def test_division(self):
        assert parse('1 / 2') == [Symbol('/'), 1, 2]

    def test_precedence_of_mult_expr(self):
        assert parse('2 * 5 + 2') == [Symbol('+'), [Symbol('*'), 2, 5], 2]
        assert parse('2 / 5 + 2') == [Symbol('+'), [Symbol('/'), 2, 5], 2]

    def test_expression_with_parentheses(self):
        assert parse('(2 + 4)') == [Symbol('+'), 2, 4]

    def test_precedence_using_parentheses(self):
        assert parse('(2 + 5) * 3') == [Symbol('*'), [Symbol('+'), 2, 5], 3]

    def test_expression_with_variables(self):
        assert parse('foo + bar + 2') == [Symbol('+'), [Symbol('+'), Symbol('foo'), Symbol('bar')], 2]


class TestFunctionCall:
    def test_basic_function_call(self):
        assert parse('foo()') == [Symbol('foo')]
        assert parse('foo(1)') == [Symbol('foo'), [1]]
        assert parse('foo(1, 2)') == [Symbol('foo'), [1, 2]]

    def test_function_call_exp_as_argument(self):
        assert parse('foo(1+2, 8*5)') == [Symbol('foo'), [[Symbol('+'), 1, 2], [Symbol('*'), 8, 5]]]

    def test_function_call_variable_as_argument(self):
        assert parse('foo(bar)') == [Symbol('foo'), [Symbol('bar')]]


class TestAssignment:
    def test_assignment_number(self):
        assert parse('foo = 1') == [Symbol('='), Symbol('foo'), 1]

    def test_assignment_expr(self):
        assert parse('bar = 1 + 2') == [Symbol('='), Symbol('bar'), [Symbol('+'), 1, 2]]
        assert parse('bar = 1 * 2') == [Symbol('='), Symbol('bar'), [Symbol('*'), 1, 2]]
        assert parse('bar = (1 + 2) * 5') == [Symbol('='), Symbol('bar'), [Symbol('*'), [Symbol('+'), 1, 2], 5]]

    def test_assigment_function(self):
        assert parse('bar = foo(1)') == [Symbol('='), Symbol('bar'), [Symbol('foo'), [1]]]
        assert parse('bar = foo(1, 2)') == [Symbol('='), Symbol('bar'), [Symbol('foo'), [1, 2]]]
