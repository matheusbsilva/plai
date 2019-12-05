import pandas as pd

from .columns import Col


def drop(dataframe, columns=None):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be instance of DataFrame')

    if not isinstance(columns, list):
        columns = [columns]

    if not all(isinstance(col, Col) for col in columns):
        raise TypeError('column must be instance of Col')
    cols = [col.name for col in columns]

    return dataframe.drop(columns=cols)
