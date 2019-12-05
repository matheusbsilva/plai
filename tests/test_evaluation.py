import pandas as pd
import pytest

from plai.interpreter import run
from plai.modules import Col
from plai.modules import drop
from plai.environment import env
from plai.symbol import Symbol


class TestAssigment:
    def test_assign_variable_add_to_env(self):
        e = env()
        run('x = 1', e)
        assert e[Symbol('x')] == 1

    def test_assing_varible_using_expr(self):
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


class TestPipeline:
    def test_pipeline_returns_dataframe(self):
        assert isinstance(run('pipeline(df): drop(.name)'), pd.DataFrame)

    def test_pipeline_raise_error_on_undeclared_dataframe(self):
        with pytest.raises(NameError):
            run('pipeline(df): drop(.name)')

    def test_pipeline_execute_stmts(self, dataframe):
        assert run('pipeline(df): drop(.name)').equals(drop(dataframe, Col('name')))
