import pandas as pd

from .columns import Col


def read_file(path, **kwargs):
    sep = ','

    return pd.read_csv(path, sep=sep)


def export_csv(dataframe, export_path):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('dataframe must be instance of DataFrame')

    dataframe.to_csv(export_path, index=False)
