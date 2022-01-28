import pytest
import pandas as pd

from plai.interpreter import run
from plai.modules import Col
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

    def test_dict(self):
        assert run("{'foo': 'bar', 'fuzz': 42}") == {'foo': 'bar', 'fuzz': 42}


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
            src = """
pipeline(fuzz):
    .name + 'bar'
"""
            run(src)

    def test_pipeline_execute_stmts(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe.copy()
        src = """
pipeline(df):
    .name + 'bar' as name
"""
        res = run(src, env=e)

        dataframe.name = dataframe.name + 'bar'

        assert res.equals(dataframe)

    def test_pipeline_execute_multiple_stmts(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe.copy()

        src = """
pipeline(df):
    .name + 'bar' as name
    .floats + 1 as floats
"""

        dataframe.name = dataframe.name + 'bar'
        dataframe.floats = dataframe.floats + 1

        assert run(src, env=e).equals(dataframe)

    def test_pipeline_with_function_call(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe.copy()
        src = """
pipeline(df):
    pd.to_datetime(.dates) as dates
"""
        result = run(src, env=e)
        dataframe.dates = pd.to_datetime(dataframe.dates)

        assert result.equals(dataframe)


class TestAliasEvaluation:
    def test_alias_change_column_name(self, dataframe):
        df_result = dataframe.assign(foo=dataframe.name)
        result = run('.name as foo',  **{'dataframe': dataframe})

        assert result.equals(df_result)

    def test_alias_create_column_with_expr_result(self, dataframe):
        df_result = dataframe.assign(foo=dataframe.name + '_foo')
        result = run(".name + '_foo' as foo", dataframe=dataframe)

        assert result.equals(df_result)


class TestColEvaluation:
    def test_sugar_col_returns_Col_instance(self, dataframe):
        e = env()
        df_symbol = Symbol('df')
        e[df_symbol] = dataframe.copy()

        assert isinstance(run('.col', dataframe=df_symbol), Col)

    def test_sugar_col_returns_Col_with_right_name(self, dataframe):
        e = env()
        df_symbol = Symbol('df')
        e[df_symbol] = dataframe.copy()

        col = run('.col', dataframe=df_symbol)
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
    .name + 'bar' as name
""" % path

        df_res = read_file(path)
        df_res.name = df_res.name + 'bar'

        assert run(src).equals(df_res)


class TestAttrCall:
    def test_attr_call_on_var(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        assert run('df.columns.shape') == (4,)


class TestSliceDataframe:
    def test_slice_dataframe_operation(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        src = """
pipeline(df):
    {.name, .number}
"""

        assert run(src, env=e).equals(dataframe[['name', 'number']])

    def test_invalid_slice_dataframe_operation(self, dataframe):
        with pytest.raises(ValueError):
            e = env()
            e[Symbol('df')] = dataframe

            src = """
pipeline(df):
    {.name, 1}
"""

            run(src, env=e)


class TestTypedDataframe:
    def setup_env(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe
        return e

    def test_type_matching_on_dataframe_load_into_var(self, csv_file_comma):
        df_type = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str'
        }
        e = env()
        e[Symbol('t')] = df_type
        path = str(csv_file_comma)

        src = """
t::df = read_file("%s")
""" % path
        run(src, env=e)
        result = e[Symbol('df')]

        assert result.equals(read_file(path))

    def test_type_matching_dataframe_schema(self, dataframe):
        df_type = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str'
        }

        env = self.setup_env(dataframe)
        env[Symbol('t')] = df_type

        src = "t::df"

        run(src, env=env)
        result = env[Symbol('df')]

        assert result.equals(dataframe)

    def test_type_not_matching_dataframe_schema(self, dataframe):
        df_type = {
            'name': 'float',
            'floats': 'int',
            'dates': 'str',
            'number': 'int'
        }

        env = self.setup_env(dataframe)
        env[Symbol('t')] = df_type

        src = "t::df"

        with pytest.raises(ValueError):
            run(src, env=env)

    def test_column_not_present_on_dataframe_schema(self, dataframe):
        df_type = {
            'foo': 'int'
        }

        env = self.setup_env(dataframe)
        env[Symbol('t')] = df_type

        src = "t::df"

        with pytest.raises(ValueError):
            run(src, env=env)

    def test_type_on_expr(self, csv_file_comma):
        df = read_file(csv_file_comma)

        df_type = {
            'name': 'str',
            'number': 'int'
        }

        env = self.setup_env(df)
        env[Symbol('t')] = df_type

        src = f"t::read_file('{csv_file_comma}')"
        assert run(src).equals(df)

    def test_typed_stmt_is_not_a_dataframe(self):
        df_type = {
            'name': 'str',
            'number': 'int'
        }
        e = env()
        e[Symbol('t')] = df_type

        with pytest.raises(TypeError):
            run("t::'foo'")


class TestOutputStmtPipeline:
    def setup_env(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe
        return e

    def test_csv_output_stmt_for_multiple_line_pipeline(self, dataframe, tmp_path):
        env = self.setup_env(dataframe)
        path = tmp_path / 'test.csv'

        src = """
pipeline(df) as '{path}':
    .name + '_foo' as foo_name
""".format(path=path)

        run(src, env=env)
        dataframe['foo_name'] = dataframe.name + '_foo'
        result_file = pd.read_csv(path)

        assert result_file.equals(dataframe)

    def test_csv_output_stmt_for_single_line_pipeline(self,
                                                      dataframe,
                                                      tmp_path):
        env = self.setup_env(dataframe)
        path = tmp_path / 'test.csv'

        src = "pipeline(df) as '{path}': .name + '_foo' as foo_name".format(path=path)

        run(src, env=env)
        dataframe['foo_name'] = dataframe.name + '_foo'
        result_file = pd.read_csv(path)

        assert result_file.equals(dataframe)

    def test_output_for_other_files_type(self, dataframe, tmp_path):
        self.setup_env(dataframe)
        path = tmp_path / 'test.xlsx'

        src = "pipeline(df) as '{path}': .name + '_foo' as foo_name".format(path=path)

        with pytest.raises(ValueError):
            run(src)

    def test_var_output_stmt_for_multiple_line_pipeline(self, dataframe):
        env = self.setup_env(dataframe)

        src = """
pipeline(df) as foo:
    .name + '_foo' as foo_name
"""

        run(src, env=env)
        dataframe['foo_name'] = dataframe.name + '_foo'
        result = env[Symbol('foo')]

        assert result.equals(dataframe)

    def test_var_output_stmt_for_single_line_pipeline(self, dataframe):
        env = self.setup_env(dataframe)

        src = "pipeline(df) as foo: .name + '_foo' as foo_name"

        run(src, env=env)
        dataframe['foo_name'] = dataframe.name + '_foo'
        result = env[Symbol('foo')]

        assert result.equals(dataframe)

    def test_invalid_typed_output_df_argument(self, dataframe):
        env = self.setup_env(dataframe)
        df_output = {
            'foo': 'int'
        }
        env[Symbol('t')] = df_output

        src = "t::pipeline(df): .name + '_foo' as foo_name"

        with pytest.raises(ValueError):
            run(src, env=env)

    def test_valid_typed_output_df_argument(self, dataframe):
        env = self.setup_env(dataframe)

        df_output = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str'
        }

        env[Symbol('t')] = df_output

        src = "t::pipeline(df): .name + '_foo' as foo_name"

        run(src, env=env)
        dataframe['foo_name'] = dataframe.name + '_foo'
        result = env[Symbol('df')]

        assert result.equals(dataframe)

    def test_input_output_df_validation(self, dataframe):
        env = self.setup_env(dataframe)

        df_input = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str'
        }

        df_output = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str',
            'foo_name': 'str'
        }

        env[Symbol('input_t')] = df_input
        env[Symbol('output_t')] = df_output

        src = """
input_t::df
output_t::pipeline(df): .name + '_foo' as foo_name
"""

        run(src, env=env)
        dataframe['foo_name'] = dataframe.name + '_foo'
        result = env[Symbol('df')]

        assert result.equals(dataframe)

    def test_invalid_input_output_df_validation(self, dataframe):
        env = self.setup_env(dataframe)

        df_input = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str'
        }

        df_output = {
            **df_input,
            'foo_name': 'int'
        }

        env[Symbol('input_t')] = df_input
        env[Symbol('output_t')] = df_output

        src = """
input_t::df
output_t::pipeline(df): .name + '_foo' as foo_name
"""

        with pytest.raises(ValueError):
            run(src, env=env)


class TestTypeStmt:
    def test_basic_type_stmt(self):
        e = env()

        run("type foo = {'col': 'float64'}", e)

        assert e[Symbol('foo')] == {'col': 'float64'}

    def test_type_expr_is_not_dict(self):
        with pytest.raises(ValueError):
            run("type foo = 'bar'")


class TestAttrCallOnDataframe:
    def test_attr_call_on_datafram_for_pipeline(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        src = "pipeline(df): $.shape"

        assert run(src, env=e) == dataframe.shape

    def test_function_attr_call_on_dataframe_for_pipeline(self, dataframe):
        e = env()
        e[Symbol('df')] = dataframe

        src = "pipeline(df): $.reset_index()"

        assert run(src, env=e).equals(dataframe.reset_index())
