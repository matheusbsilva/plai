import pytest

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
