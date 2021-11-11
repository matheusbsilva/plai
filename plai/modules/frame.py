import pandas as pd

from .columns import Col


def drop(*columns, **kwargs):
    if 'dataframe' not in kwargs:
        raise ValueError('Dataframe not present in the scope')

    if not all(isinstance(col, Col) for col in columns):
        raise TypeError('column must be instance of Col')

    dataframe = kwargs['dataframe']

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be instance of DataFrame')

    cols = [col.name for col in columns]

    return dataframe.drop(columns=cols)


def read_file(path, **kwargs):
    sep = ','

    return pd.read_csv(path, sep=sep)


def export_csv(dataframe, export_path):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be instance of DataFrame')

    path = dataframe.to_csv(export_path, index=False)

    return path


def dropna(*columns, **kwargs):
    if 'dataframe' not in kwargs:
        raise ValueError('Dataframe not present in the scope')

    dataframe = kwargs['dataframe']

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be instance of DataFrame')

    if not all(isinstance(col, Col) for col in columns):
        raise TypeError('column must be instance of Col')

    columns = [col.name for col in columns]

    if not columns:
        columns = None

    return dataframe.dropna(subset=columns)
