import os

import pandas as pd
import numpy as np
import pytest

from plai.modules import Col
from plai.modules import read_file
from plai.modules import export_csv
from plai.modules import PyImporter


class TestCol:
    def test_col_name_attribution(self, dataframe):
        c = Col('name', dataframe)
        assert c.name == 'name'

    def test_col_call_on_dataframe(self, dataframe):
        column = Col('name', dataframe)
        assert np.array_equal(column(), ['foo', 'bar'])

    def test_col_sum_operation(self, dataframe):
        column = Col('name', dataframe)
        result = column + '_fuzz'

        assert np.array_equal(result, ['foo_fuzz', 'bar_fuzz'])

    def test_col_sum_col_operation(self, dataframe):
        column = Col('name', dataframe)
        column_b = Col('dates', dataframe)

        result = column + column_b

        assert result.equals(dataframe.name + dataframe.dates)

    def test_col_minus_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column - 1

        assert np.array_equal(result, [0, 1])

    def test_col_minus_col_operation(self, dataframe):
        column = Col('number', dataframe)
        column_b = Col('floats', dataframe)
        result = column - column_b

        assert result.equals(dataframe.number - dataframe.floats)

    def test_col_mul_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column * 2

        assert np.array_equal(result, [2, 4])

    def test_col_mul_col_operation(self, dataframe):
        column = Col('number', dataframe)
        column_b = Col('floats', dataframe)
        result = column * column_b

        assert result.equals(dataframe.number * dataframe.floats)

    def test_col_true_div_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column / 2.0

        assert np.array_equal(result, [.5, 1])

    def test_col_true_div_col_operation(self, dataframe):
        column = Col('number', dataframe)
        column_b = Col('floats', dataframe)
        result = column / column_b

        assert result.equals(dataframe.number / dataframe.floats)

    def test_col_floor_div_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column // 2

        assert np.array_equal(result, [0, 1])

    def test_col_floor_div_col_operation(self, dataframe):
        column = Col('number', dataframe)
        column_b = Col('floats', dataframe)
        result = column // column_b

        assert result.equals(dataframe.number // dataframe.floats)

    def test_gt_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column > 1

        assert result.equals(pd.Series([2], index=[1]))

    def test_ge_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column >= 1

        assert result.equals(pd.Series([1, 2], index=[0, 1]))

    def test_lt_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column < 2

        assert result.equals(pd.Series([1], index=[0]))

    def test_le_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column <= 2

        assert result.equals(pd.Series([1, 2], index=[0, 1]))

    def test_eq_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column == 2

        assert result.equals(pd.Series([2], index=[1]))

    def test_ne_operation(self, dataframe):
        column = Col('number', dataframe)
        result = column != 2

        assert result.equals(pd.Series([1], index=[0]))

    def test_contains_full_match_operation(self, dataframe):
        column = Col('name', dataframe)
        result = column.contains('foo')

        assert result.equals(pd.Series(['foo'], index=[0]))

    def test_get_attr_on_column(self, dataframe):
        column = Col('name', dataframe)

        assert column.str.upper().equals(dataframe.name.str.upper())


class TestDataFrameBuiltinFunctions:

    def test_read_file_function_returns_dataframe_for_csv_comma(self, dataframe, csv_file_comma):
        path = str(csv_file_comma)

        assert isinstance(read_file(path), pd.DataFrame)
        assert read_file(path).equals(pd.read_csv(path, sep=','))

    def test_read_file_function_return_dataframe_for_csv_semicolon(self, dataframe, csv_file_semicolon):
        path = str(csv_file_semicolon)

        assert isinstance(read_file(path), pd.DataFrame)

    def test_export_csv_invalid_dataframe_type(self):
        with pytest.raises(TypeError):
            export_csv('foo', 'bar')

    def test_export_csv(self, dataframe, tmp_path):

        expected_path = tmp_path / 'expected.csv'
        result_path = tmp_path / 'result.csv'

        dataframe.to_csv(expected_path, index=False)
        export_csv(dataframe, result_path)

        assert pd.read_csv(result_path).equals(pd.read_csv(expected_path))


class TestPyImporter:
    def test_module_import(self):
        py = PyImporter()

        assert py.os.path._module == os.path

    def test_nested_funcion_import(self):
        py = PyImporter()

        assert py.pandas.api.types.is_object_dtype == pd.api.types.is_object_dtype

    def test_import_specifying_module(self):
        py = PyImporter(module=os)

        assert py.path == os.path

    def test_repr_with_module(self):
        py = PyImporter(module=os)

        assert py.__repr__() == f"PyImporter('', {os})"

    def test_repr_without_module(self):
        py = PyImporter('os')

        assert py.__repr__() == "PyImporter('os')"
