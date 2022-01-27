import pytest

from lark.exceptions import UnexpectedToken
from plai.parser import parse
from plai.symbol import Symbol


class TestBasicTokens:
    def test_token_number(self):
        assert parse('7') == 7
        assert parse('8.1') == 8.1
        assert parse('.5') == 0.5
        assert parse('1e+1') == 10.0
        assert parse('0b10') == 2
        assert parse('1j') == 1j

    def test_token_string(self):
        assert parse('"hello"') == "hello"
        assert parse("'hello'") == "hello"
        assert parse('"hello world"') == "hello world"
        assert parse('b"\x41"') == b"A"
        assert parse("r'hello\\nworld'") == r"hello\nworld"

    def test_escaped_token_string(self):
        assert parse(r'"hello \"world\""') == 'hello "world"'
        assert parse(r'"hello \n world"') == "hello \n world"
        assert parse(r'"hello \t world"') == "hello \t world"
        assert parse(r'"hello \r world"') == "hello \r world"

    def test_const_true(self):
        assert parse('True') is True

    def test_const_false(self):
        assert parse('False') is False

    def test_const_none(self):
        assert parse('None') is None

    def test_variable_call(self):
        assert parse('bar') == Symbol('bar')

    def test_attribute_call(self):
        assert parse('bar.foo') == [Symbol.ATTR, Symbol('bar'), Symbol('foo')]

    def test_list(self):
        assert parse('[1, 2]') == [Symbol.LIST, 1, 2]

    def test_dict(self):
        assert parse("{'foo': 'bar', 'fuzz': 42}") == [
            Symbol.DICT, ['foo', 'bar'], ['fuzz', 42]
        ]


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

    def test_not_expression(self):
        assert parse('not 1') == [Symbol('not'), 1]
        assert parse('not 0') == [Symbol('not'), 0]
        assert parse('not "test"') == [Symbol('not'), 'test']

    def test_and_expression(self):
        assert parse('1 and 0') == [Symbol('and'), 1, 0]

    def test_or_expression(self):
        assert parse('1 or 0') == [Symbol('or'), 1, 0]

    def test_comparison_expression(self):
        assert parse('1 > 2') == [Symbol('>'), 1, 2]
        assert parse('1 < 2') == [Symbol('<'), 1, 2]
        assert parse('1 >= 2') == [Symbol('>='), 1, 2]
        assert parse('1 <= 2') == [Symbol('<='), 1, 2]
        assert parse('1 == 2') == [Symbol('=='), 1, 2]
        assert parse('1 != 2') == [Symbol('!='), 1, 2]

    def test_compose_comparison_expression(self):
        assert parse('1 > 2 + 1') == [Symbol('>'), 1, [Symbol('+'), 2, 1]]

    def test_expression_with_variables(self):
        assert parse('foo + bar + 2') == [Symbol('+'), [Symbol('+'),
                                                        Symbol('foo'),
                                                        Symbol('bar')], 2]

    def test_sum_using_functions(self):
        assert parse('foo() + bar() + 1') == [Symbol('+'), [
            Symbol('+'), [Symbol.FUNCTION, Symbol('foo')], [Symbol.FUNCTION, Symbol('bar')]], 1]

    def test_precedence_using_functions(self):
        assert parse('(foo() + bar()) * 2') == [Symbol('*'), [
            Symbol('+'), [Symbol.FUNCTION, Symbol('foo')], [Symbol.FUNCTION, Symbol('bar')]], 2]

    def test_sum_using_strings(self):
        assert parse('"hello" + "world"') == [Symbol('+'), 'hello', 'world']

    def test_sum_using_attr_call(self):
        assert parse('foo.bar + fuzz.buzz') == [
            Symbol('+'),
            [Symbol.ATTR, Symbol('foo'), Symbol('bar')],
            [Symbol.ATTR, Symbol('fuzz'), Symbol('buzz')]
        ]


class TestStmts:
    def test_multiple_stmts_newline_presence(self):
        stmts = """
a = 2
b = 3
"""
        assert parse(stmts) == [
            Symbol.BEGIN,
            [Symbol.ASSIGNMENT, Symbol('a'), 2],
            [Symbol.ASSIGNMENT, Symbol('b'), 3]
        ]

    def test_one_stmt(self):
        assert parse('1 + 1') == [Symbol('+'), 1, 1]


class TestTypeDefinition:
    def test_basic_type_definition(self):
        assert parse("type df_type = {'col': 'float64'}") == [
            Symbol.TYPE, Symbol('df_type'), [Symbol.DICT, ['col', 'float64']]
        ]


class TestFunctionCall:
    def test_basic_function_call(self):
        assert parse('foo()') == [Symbol.FUNCTION, Symbol('foo')]

    def test_function_call_exp_as_argument(self):
        assert parse('foo(1+2, 8*5)') == [Symbol.FUNCTION, Symbol('foo'),
                                          [Symbol('+'), 1, 2],
                                          [Symbol('*'), 8, 5], []
                                          ]

    def test_function_call_passing_string_as_argument(self):
        assert parse('foo("bar")') == [Symbol.FUNCTION, Symbol('foo'), 'bar', []]

    def test_function_call_variable_as_argument(self):
        assert parse('foo(bar)') == [Symbol.FUNCTION, Symbol('foo'), Symbol('bar'), []]

    def test_function_call_sugar_column_as_argument(self):
        assert parse('foo(.col)') == [Symbol.FUNCTION, Symbol('foo'), [Symbol.COLUMN, 'col'], []]

    def test_funcion_call_attr_call_as_argument(self):
        assert parse('foo(bar.fuzz)') == [Symbol.FUNCTION, Symbol('foo'), [Symbol.ATTR, Symbol('bar'), Symbol('fuzz')], []]

    def test_function_call_function_as_argument(self):
        assert parse('foo(bar())') == [Symbol.FUNCTION, Symbol('foo'), [Symbol.FUNCTION, Symbol('bar')], []]

    def test_function_call_mixed_arguments(self):
        assert parse('foo(1, 1+2, x)') == [Symbol.FUNCTION, Symbol('foo'), 1, [Symbol('+'), 1, 2], Symbol('x'), []]

    def test_function_call_named_argument(self):
        assert parse('foo(bar=42)') == [Symbol.FUNCTION, Symbol('foo'), [[Symbol('bar'), 42]]]
        assert parse('foo(bar=42, buzz=55)') == [
            Symbol.FUNCTION,
            Symbol('foo'),
            [[Symbol('bar'), 42], [Symbol('buzz'), 55]]
        ]

    def test_function_call_position_and_named_arguments(self):
        assert parse('foo(42, bar=55)') == [
            Symbol.FUNCTION,
            Symbol('foo'), 42, [[Symbol('bar'), 55]]
        ]

    def test_one_line_typed_stmt(self):
        assert parse('t::df') == [Symbol.TYPED, Symbol('t'), Symbol('df')]

    def test_multiline_line_typed_stmt(self):
        src = """
t::df
"""
        assert parse(src) == [Symbol.TYPED, Symbol('t'), Symbol('df')]


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

    def test_assignment_function(self):
        assert parse('bar = foo(1)') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                         [Symbol.FUNCTION, Symbol('foo'), 1, []]]
        assert parse('bar = foo(1, 2)') == [Symbol.ASSIGNMENT, Symbol('bar'),
                                            [Symbol.FUNCTION, Symbol('foo'), 1, 2, []]]


class TestPipeline:
    def test_pipeline_declaration(self):
        src = """
pipeline(bar):
    foo()
"""
        assert parse(src) == [
            Symbol.PIPELINE,
            [Symbol('bar')],
            [[Symbol.FUNCTION, Symbol('foo')]]
        ]

    def test_sugar_column_call(self):
        assert parse('.col') == [Symbol.COLUMN, 'col']
        assert parse('."col"') == [Symbol.COLUMN, 'col']

    def test_invalid_sugar_column_call(self):
        assert parse('.1') != [Symbol.COLUMN, 1]

        with pytest.raises(UnexpectedToken):
            parse('.()')

    def test_one_line_stmt_on_pipeline(self):
        assert parse('pipeline(df): .col + 1') == [
            Symbol.PIPELINE,
            [Symbol('df')],
            [[Symbol('+'), [Symbol.COLUMN, 'col'], 1]]
        ]

    def test_one_line_stmts_on_pipeline(self):
        res = parse('pipeline(df): .col + 1;.col + 2')
        assert res == [
            Symbol.PIPELINE,
            [Symbol('df')],
            [
                [Symbol('+'), [Symbol.COLUMN, 'col'], 1],
                [Symbol('+'), [Symbol.COLUMN, 'col'], 2]
            ]
        ]

    def test_multiple_stmts_on_pipeline(self):
        src = """
pipeline(bar):
    foo(.bar)
    fuzz(.bar)
"""
        parsed = parse(src)
        assert parsed == [
            Symbol.PIPELINE,
            [Symbol('bar')],
            [
                [Symbol.FUNCTION, Symbol('foo'), [Symbol.COLUMN, 'bar'], []],
                [Symbol.FUNCTION, Symbol('fuzz'), [Symbol.COLUMN, 'bar'], []]
            ]
        ]

    def test_sugar_column_expression(self):
        assert parse('.col + 1') == [Symbol('+'), [Symbol.COLUMN, 'col'], 1]

    def test_as_operator(self):
        assert parse('.col as foo') == [
            Symbol.ALIAS,
            [Symbol.COLUMN, 'col'],
            Symbol('foo')
        ]

    def test_list_columns(self):
        assert parse('[.col, .col2]') == [
            Symbol.LIST,
            [Symbol.COLUMN, 'col'],
            [Symbol.COLUMN, 'col2']
        ]

    def test_slice_dataframe(self):
        assert parse('{.col, .col2}') == [
            Symbol.SLICE_DF,
            [Symbol.COLUMN, 'col'],
            [Symbol.COLUMN, 'col2']
        ]

    def test_var_output_stmt_multiple_line_for_pipeline(self):
        src = """
pipeline(df) as foo:
    .name as foo_name
"""
        assert parse(src) == [
            Symbol.OUTPUT,
            Symbol('foo'),
            [
                Symbol.PIPELINE,
                [Symbol('df')],
                [
                    [Symbol.ALIAS, [Symbol.COLUMN, 'name'], Symbol('foo_name')]
                ]
            ]
        ]

    def test_var_output_stmt_single_line_for_pipeline(self):
        src = "pipeline(df) as foo: .name as foo_name"
        assert parse(src) == [
            Symbol.OUTPUT,
            Symbol('foo'),
            [
                Symbol.PIPELINE,
                [Symbol('df')],
                [
                    [Symbol.ALIAS, [Symbol.COLUMN, 'name'], Symbol('foo_name')]
                ]
            ]
        ]

    def test_string_output_stmt_multiple_line_for_pipeline(self):
        src = """
pipeline(df) as 'test.csv':
    .name as foo_name
"""
        assert parse(src) == [
            Symbol.OUTPUT,
            'test.csv',
            [
                Symbol.PIPELINE,
                [Symbol('df')],
                [
                    [Symbol.ALIAS, [Symbol.COLUMN, 'name'], Symbol('foo_name')]
                ]
            ]
        ]

    def test_string_output_stmt_single_line_for_pipeline(self):
        src = "pipeline(df) as 'test.csv': .name as foo_name"
        assert parse(src) == [
            Symbol.OUTPUT,
            'test.csv',
            [
                Symbol.PIPELINE,
                [Symbol('df')],
                [
                    [Symbol.ALIAS, [Symbol.COLUMN, 'name'], Symbol('foo_name')]
                ]
            ]
        ]

    def test_typed_output_df_argument(self):
        src = "output_type::pipeline(df): .name as foo_name"
        assert parse(src) == [
            Symbol.TYPED,
            Symbol('output_type'),
            [
                Symbol.PIPELINE,
                [Symbol('df')],
                [
                    [Symbol.ALIAS, [Symbol.COLUMN, 'name'], Symbol('foo_name')]
                ],
            ]
        ]

    def test_dataframe_attr_call(self):
        src = "$.bar"

        assert parse(src) == [Symbol.DF_ATTR_CALL, Symbol('bar')]

    def test_dataframe_attr_call_function(self):
        src = "$.foo()"

        assert parse(src) == [
            Symbol.FUNCTION, [Symbol.DF_ATTR_CALL, Symbol('foo')]
        ]
