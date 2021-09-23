import pandas as pd
import pytest

from plai.interpreter import run
from plai.modules import Col
from plai.modules import drop
from plai.modules import read_file
from plai.environment import env
from plai.symbol import Symbol


class TestAssigment:
    def test_assign_variable_add_to_env(self):
        e = env()
        run('x = 1', e)
        assert e[Symbol('x')] == 1

    def test_assing_variable_using_expr(self):
        e = env()
        run('x = 1 + 2 + 3', e)
        assert e[Symbol('x')] == 6


class TestExpressions:
    def test_number_sum_expressions(self):
        assert run('1 + 2') == 3
        assert run('1 + 2 + 3') == 6

    def test_number_sub_expression(self):
        assert run('1 - 2') == -1
        assert run('10 - 2 - 1') == 7

    def test_number_mult_expression(self):
        assert run('2 * 3') == 6
        assert run('2 * 3 * 4') == 24

    def test_number_div_expression(self):
        assert run('6 / 2') == 3
        assert run('12 / 2 / 3') == 2

    def test_precedence_number_expression(self):
        assert run('2 * 3 + 5') == 11
        assert run('2 / 2 + 3') == 4

    def test_precedence_with_parentheses_number_expression(self):
        assert run('(2 + 3) * 5') == 25
        assert run('(6 / 2) * 6') == 18


class TestFunctionCall:
    def test_function_call_without_arguments(self):
        e = env()

        def foo():
            return 42

        e[Symbol('foo')] = foo
        assert run('foo()', env=e) == 42

    def test_function_call_with_arguments(self):
        e = env()

        def foo(x):
            return x * 2
        e[Symbol('foo')] = foo

        assert run('foo(3)', env=e) == 6

    def test_function_call_with_named_arguments(self):
        e = env()

        def foo(x, z=0, y=10):
            return x * z

        e[Symbol('foo')] = foo

        assert run('foo(3, z=2)', env=e) == 6


class TestPipeline:
    def test_pipeline_raise_error_on_undeclared_dataframe(self):
        with pytest.raises(NameError):
            run('pipeline(df): \n\tdrop(.name)')

    def test_pipeline_execute_stmts(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        assert run('pipeline(df): \n\tdrop(.name)', env=e).equals(
                drop(dataframe, Col('name')))

    def test_pipeline_execute_multiple_stmts(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        assert run('pipeline(df): \n\tdrop(.name) \n\tdrop(.floats)', env=e).equals(
                drop(dataframe, [Col('name'), Col('floats')]))


class TestColEvaluation:
    def test_sugar_col_returns_Col_instance(self):
        assert isinstance(run('.col'), Col)

    def test_sugar_col_returns_Col_with_right_name(self):
        col = run('.col')
        assert col.name == 'col'


class TestMultipleStmts:
    def test_multiple_stmts_with_pipeline(self, dataframe, csv_file_comma):
        path = str(csv_file_comma)

        src = """
        df = read_file("%s")
        pipeline(df):
            drop(.name)
        """ % path

        df_res = read_file(path)
        result = drop(df_res, Col('name'))

        assert run(src).equals(result)


class TestAttrCall:
    def test_attr_call_on_var(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        assert run('df.columns').equals(dataframe.columns)
