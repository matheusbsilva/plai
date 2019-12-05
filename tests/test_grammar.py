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

    def test_attribute_call(self):
        assert parse('bar.foo') == [Symbol.ATTR, Symbol('bar'), Symbol('foo')]


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
        assert parse('foo + bar + 2') == [Symbol('+'), [Symbol('+'),
                                                        Symbol('foo'),
                                                        Symbol('bar')], 2]

    def test_sum_using_functions(self):
        assert parse('foo() + bar() + 1') == [Symbol('+'), [
            Symbol('+'), [Symbol('foo')], [Symbol('bar')]], 1]

    def test_precedence_using_functions(self):
        assert parse('(foo() + bar()) * 2') == [Symbol('*'), [
            Symbol('+'), [Symbol('foo')], [Symbol('bar')]], 2]

    def test_sum_using_strings(self):
        assert parse('"hello" + "world"') == [Symbol('+'), 'hello', 'world']

    def test_sum_using_attr_call(self):
        assert parse('foo.bar + fuzz.buzz') == [Symbol('+'),
                [Symbol.ATTR, Symbol('foo'), Symbol('bar')],
                [Symbol.ATTR, Symbol('fuzz'), Symbol('buzz')]]


class TestFunctionCall:
    def test_basic_function_call(self):
        assert parse('foo()') == [Symbol('foo')]

    def test_function_call_exp_as_argument(self):
        assert parse('foo(1+2, 8*5)') == [Symbol('foo'), [
            [Symbol('+'), 1, 2], [Symbol('*'), 8, 5]]]

    def test_function_call_variable_as_argument(self):
        assert parse('foo(bar)') == [Symbol('foo'), [Symbol('bar')]]

    def test_function_call_sugar_column_as_argument(self):
        assert parse('foo(.col)') == [Symbol('foo'), [[
            Symbol.COLUMN, 'col']]]

    def test_funcion_call_attr_call_as_argument(self):
        assert parse('foo(bar.fuzz)') == [Symbol('foo'), [[
            Symbol.ATTR, Symbol('bar'), Symbol('fuzz')]]]

    def test_function_call_function_as_argument(self):
        assert parse('foo(bar())') == [Symbol('foo'), [[Symbol('bar')]]]

    def test_function_call_mixed_arguments(self):
        assert parse('foo(1, 1+2, x, .col, fuzz.buzz, p())') == [
                Symbol('foo'), [1, [Symbol('+'), 1, 2], Symbol('x'), [
                    Symbol.COLUMN, 'col'], [
                        Symbol.ATTR, Symbol('fuzz'), Symbol('buzz')], [
                            Symbol('p')]]
                ]


class TestAssignment:
    def test_assignment_number(self):
        assert parse('foo = 1') == [Symbol.ASSIGNMENT, Symbol('foo'), 1]

    def test_assignment_expr(self):
        assert parse('bar = 1 + 2') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                        [Symbol('+'), 1, 2]]
        assert parse('bar = 1 * 2') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                        [Symbol('*'), 1, 2]]
        assert parse('bar = (1 + 2) * 5') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                              [Symbol('*'),
                                                  [Symbol('+'), 1, 2], 5]]

    def test_assigment_function(self):
        assert parse('bar = foo(1)') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                         [Symbol('foo'), [1]]]
        assert parse('bar = foo(1, 2)') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                            [Symbol('foo'), [1, 2]]]


class TestPipeline:
    def test_pipeline_declaration(self):
        assert parse('pipeline(bar): foo()') == [Symbol.PIPELINE,
                                                 [Symbol('bar')],
                                                 [[Symbol('foo')]]]
        assert parse('pipeline(bar, fuzz): foo()') == [Symbol.PIPELINE,
                                                       [Symbol('bar'),
                                                           Symbol('fuzz')],
                                                       [[Symbol('foo')]]]

    def test_sugar_column_call(self):
        assert parse('.col') == [Symbol.COLUMN, 'col']
        assert parse('."col"') == [Symbol.COLUMN, 'col']

    def test_multiple_stmts_on_pipeline(self):
        assert parse('pipeline(bar): foo(.bar) fuzz(.bar)') == [Symbol.PIPELINE, [Symbol('bar')], [
            [Symbol('foo'), [[Symbol.COLUMN, 'bar']]], [Symbol('fuzz'), [[Symbol.COLUMN, 'bar']]]
            ]]
