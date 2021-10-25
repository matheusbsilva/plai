import operator as op

import pandas as pd

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


# TODO: find a better solution
def kwargs_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args)
    return wrapper


def _make_global_env():
    dic = {
        '+': kwargs_decorator(op.add),
        '-': kwargs_decorator(op.sub),
        '*': kwargs_decorator(op.mul),
        '/': kwargs_decorator(op.truediv),
        '//': kwargs_decorator(op.floordiv),
        '>': kwargs_decorator(op.gt),
        '<': kwargs_decorator(op.lt),
        '>=': kwargs_decorator(op.ge),
        '<=': kwargs_decorator(op.le),
        '==': kwargs_decorator(op.eq),
        'not': op.not_,
        'and': op.and_,
        'pd': pd,
        'print': print,
        'max': max,
        'min': min,
        'abs': abs,
        'round': round,
        'len': len,
        'begin': lambda *x: x[-1],
        'drop': frame.drop,
        'dropna': frame.dropna,
        'read_file': frame.read_file,
        'export_csv': frame.export_csv
    }

    global_ops = {Symbol(k): v for k, v in dic.items()}

    return global_ops


global_env = _make_global_env()
