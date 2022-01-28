import pytest
import pandas as pd

from plai.environment import env
from plai.environment import global_env
from plai.symbol import Symbol


class TestEnvironment:
    def test_env_can_be_create(self):
        assert env() is not None
        assert isinstance(env(), dict)

    def test_vars_can_be_initialized(self):
        x = Symbol('x')
        assert env({x: 3})[x] == 3

    def test_vars_can_only_be_symbols(self):
        with pytest.raises(TypeError):
            env({'x': 1})

    def test_basic_operators_exists_in_default_env(self):
        assert env() == global_env
        assert set(env({Symbol('x'): 3})).issuperset(global_env)

    def test_builtin_functions_exist_in_default_env(self):
        e = env()

        assert Symbol('read_file') in e
        assert Symbol('export_csv') in e
        assert Symbol('py') in e

    def test_pandas_available_on_env(self):
        e = env()
        pd_symbol = Symbol('pd')

        assert pd_symbol in e
        assert e[pd_symbol] == pd
