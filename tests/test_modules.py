import pandas as pd
import numpy as np
import pytest

from plai.modules import Col
from plai.modules import drop
from plai.modules import read_file
from plai.modules import dropna


class TestCol:
    def test_col_name_attribution(self):
        c = Col('name')
        assert c.name == 'name'

    def test_col_call_on_dataframe(self, dataframe):
        column = Col('name')
        assert np.array_equal(column(dataframe), ['foo', 'bar'])


class TestDataFrameBuiltinFunctions:
    def test_drop_function_one_col_as_arg(self, dataframe):
        c_name = Col('name')
        assert 'name' not in drop(dataframe, c_name).columns

    def test_drop_function_multiple_cols_as_args(self, dataframe):
        c_name = Col('name')
        c_number = Col('number')
        res_columns = drop(dataframe, [c_name, c_number]).columns

        assert set(['name', 'number']).isdisjoint(set(res_columns))

    def test_drop_function_passing_wrong_type_of_dataframe(self, dataframe):
        with pytest.raises(TypeError):
            c = Col('name')
            drop([1, 2], c)

    def test_drop_function_passing_wrong_type_of_columns(self, dataframe):
        with pytest.raises(TypeError):
            drop(dataframe, 'name')

    def test_read_file_function_returns_dataframe_for_csv_comma(self, dataframe, csv_file_comma):
        path = str(csv_file_comma)

        assert isinstance(read_file(path), pd.DataFrame)
        assert read_file(path).equals(pd.read_csv(path, sep=','))

    def test_Read_file_function_return_dataframe_for_csv_semicolon(self, dataframe, csv_file_semicolon):
        path = str(csv_file_semicolon)

        assert isinstance(read_file(path), pd.DataFrame)

    def test_dropna(self, dataframe):
        dataframe['x'] = [1, np.NaN]

        assert dropna(dataframe).equals(dataframe.dropna())
