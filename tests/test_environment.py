import pytest

from plai.environment import env
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
