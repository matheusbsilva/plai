import pandas as pd
import numpy as np

from plai.modules import Col


class TestCol:
    def test_col_name_attribution(self):
        c = Col('name')
        assert c.name == 'name'

    def test_col_call_on_dataframe(self):
        data = np.array(['foo', 'bar'])
        df = pd.DataFrame(data={'name': data})
        column = Col('name')

        assert np.array_equal(column(df), data)
