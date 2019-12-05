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


def read_file(path, **kwargs):
    sep = ','

    if 'sep' in kwargs:
        sep = kwargs['sep']

    return pd.read_csv(path, sep=sep)


def export_csv(dataframe, export_path):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be instance of DataFrame')

    path = dataframe.to_csv(export_path)

    return path


