import operator as op

import pandas as pd

from .symbol import Symbol
from .modules import frame
from .modules import PyImporter


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
        '//': op.floordiv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '==': op.eq,
        'not': op.not_,
        'and': op.and_,
        'or': op.or_,
        'pd': pd,
        'print': print,
        'max': max,
        'min': min,
        'abs': abs,
        'round': round,
        'len': len,
        'sum': sum,
        'begin': lambda *x: x[-1],
        'read_file': frame.read_file,
        'export_csv': frame.export_csv,
        'py': PyImporter()
    }

    global_ops = {Symbol(k): v for k, v in dic.items()}

    return global_ops


global_env = _make_global_env()
