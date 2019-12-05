import operator as op
import pandas as pd

from .parser import parse
from .symbol import Symbol
from .environment import env


def eval(sexpr, e=None):
    if e is None:
        e = env()

    if isinstance(sexpr, Symbol):
        return e[sexpr]

    elif isinstance(sexpr, (int, float, str)):
        return sexpr

    head, *args = sexpr

    if head == Symbol.ASSIGNMENT:
        var, exp = args
        e[var] = eval(exp, e)

    elif head == Symbol.PIPELINE:
        pipeline_args, block = args

        return pd.DataFrame()

    else:
        proc = eval(head, e)
        vals = [eval(arg, e) for arg in args]

        return proc(*vals)


def run(src, env=None):
    return eval(parse(src), env)
