import pytest
import pandas as pd


def create_csv_file(tmpdir_factory, sep=','):
    content = """\
name{sep}number{sep}floats{sep}dates
foo{sep}1{sep}1.5{sep}2019-01-01
bar{sep}2{sep}2.5{sep}2019-02-02
buz{sep}3{sep}3.5{sep}2019-03-03
    """
    file = tmpdir_factory.mktemp('files').join('test.csv')
    file.write(content.format(sep=sep))

    return file


@pytest.fixture
def dataframe():
    df = pd.DataFrame(data={'name': ['foo', 'bar'],
                            'number': [1, 2],
                            'floats': [2.5, 3.4],
                            'dates': ['2019-01-01', '2019-06-01']
                            })

    return df


@pytest.fixture(scope='session')
def csv_file_comma(tmpdir_factory):
    return create_csv_file(tmpdir_factory)


@pytest.fixture(scope='session')
def csv_file_semicolon(tmpdir_factory):
    return create_csv_file(tmpdir_factory, sep=';')
