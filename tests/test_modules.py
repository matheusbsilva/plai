import pandas as pd
import numpy as np
import pytest

from plai.modules import Col
from plai.modules import drop


@pytest.fixture
def dataframe():
    df = pd.DataFrame(data={'name': ['foo', 'bar'],
                            'number': [1, 2],
                            'floats': [2.5, 3.4],
                            'dates': ['2019-01-01', '2019-10-06']})

    return df


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

    def test_drop_function_passing_empty_columns(self, dataframe):
        with pytest.raises(ValueError):
            drop(dataframe)
