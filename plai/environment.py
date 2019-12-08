import operator as op

from .symbol import Symbol
from .modules import frame


def env(variables=None):
    env = global_env

    if variables:
        if any(not isinstance(key, Symbol) for key in variables):
            raise TypeError('variables must be instance of Symbol')
        env.update(variables)
        return env
    else:
        return env


def _make_global_env():
    dic = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        'drop': frame.drop,
        'dropna': frame.dropna,
        'read_file': frame.read_file,
        'export_csv': frame.export_csv,
    }

    global_ops = {Symbol(k): v for k, v in dic.items()}

    return global_ops


global_env = _make_global_env()
