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

    def test_comparison_expression(self):
        assert run('1 > 1') is False
        assert run('1 >= 1') is True
        assert run('2 < 2') is False
        assert run('2 <= 2') is True

    def test_not_expression(self):
        assert run('not 1') is False
        assert run('not 0') is True
        assert run('not "foo"') is False

    def test_and_expression(self):
        assert run('1 and 1') == 1
        assert run('1 and 0') == 0

    def test_or_expression(self):
        assert run('1 or 1') == 1
        assert run('1 or 0') == 1
        assert run('0 or 0') == 0

    def test_bool_constants(self):
        assert run('True') is True
        assert run('False') is False

    def test_none_constant(self):
        assert run('None') is None

    def test_list(self):
        assert run('[1, 2]') == [1, 2]


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

    @pytest.mark.skip(reason='Operation not supported yet')
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
            drop(Col('name', dataframe), **{'dataframe': dataframe}))

    def test_pipeline_execute_multiple_stmts(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        assert run('pipeline(df): \n\tdrop(.name) \n\tdrop(.floats)', env=e).equals(
            drop(Col('name', dataframe), Col('floats', dataframe), **{'dataframe': dataframe}))


class TestAliasEvaluation:
    def test_alias_change_column_name(self, dataframe):
        df_result = dataframe.assign(foo=dataframe.name)
        result = run('.name as foo',  **{'dataframe': dataframe})

        assert result.equals(df_result)

    def test_alias_create_column_with_expr_result(self, dataframe):
        df_result = dataframe.assign(foo=dataframe.name + '_foo')
        result = run(".name + '_foo' as foo", **{'dataframe': dataframe})

        assert result.equals(df_result)


class TestColEvaluation:
    def test_sugar_col_returns_Col_instance(self, dataframe):
        e = env()
        df_symbol = Symbol('df')
        e[df_symbol] = dataframe

        assert isinstance(run('.col', **{'dataframe': df_symbol}), Col)

    def test_sugar_col_returns_Col_with_right_name(self, dataframe):
        e = env()
        df_symbol = Symbol('df')
        e[df_symbol] = dataframe

        col = run('.col', **{'dataframe': df_symbol})
        assert col.name == 'col'


class TestRowByRowOperations:
    def test_row_arithmetic_operation(self, dataframe, csv_file_comma):
        path = str(csv_file_comma)

        src = """
df = read_file("%s")
pipeline(df):
    .'name' + '_foo' as name
""" % path

        df_res = read_file(path)
        df_res['name'] = df_res['name'] + '_foo'

        assert run(src).equals(df_res)

    def test_row_filter_operation(self, dataframe, csv_file_comma):
        path = str(csv_file_comma)

        src = """
df = read_file("%s")
pipeline(df):
    .name == 'foo' as name
""" % path

        df_res = read_file(path)
        df_res = df_res.assign(name=df_res.name[df_res.name == 'foo'])

        assert run(src).equals(df_res)


class TestMultipleStmts:
    def test_multiple_stmts_with_pipeline(self, dataframe, csv_file_comma):
        path = str(csv_file_comma)

        src = """
df = read_file("%s")
pipeline(df):
    drop(.name)
""" % path

        df_res = read_file(path)
        result = drop(Col('name', **{'dataframe': df_res}), **{'dataframe': df_res})

        assert run(src).equals(result)


class TestAttrCall:
    def test_attr_call_on_var(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        assert run('df.columns').equals(dataframe.columns)
