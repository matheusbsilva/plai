import operator as op
import pandas as pd

from .parser import parse
from .symbol import Symbol
from .environment import env


def eval(sexpr, environment=None):
    if environment is None:
        environment = env()

    if isinstance(sexpr, Symbol):
        return environment[sexpr]

    elif isinstance(sexpr, (int, float, str)):
        return sexpr

    head, *args = sexpr

    if head == Symbol.ASSIGNMENT:
        var, exp = args
        environment[var] = eval(exp, env)

    elif head == Symbol.PIPELINE:
        pipeline_args, block = args

        return pd.DataFrame()

    else:
        proc = eval(head, environment)
        vals = [eval(arg, environment) for arg in args]

        return proc(*vals)


def run(src, env=None):
    return eval(parse(src), env)
