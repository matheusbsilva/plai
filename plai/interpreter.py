from .parser import parse
from .symbol import Symbol
from .modules import Col
from .environment import env


def eval(sexpr, e=None):
    if e is None:
        e = env()

    if isinstance(sexpr, Symbol):
        try:
            value = e[sexpr]
        except KeyError:
            raise NameError('name %s is undefined' % sexpr)
        return value

    elif isinstance(sexpr, (int, float, str)):
        return sexpr

    head, *args = sexpr

    if head == Symbol.ASSIGNMENT:
        var, exp = args
        e[var] = eval(exp, e)

    elif head == Symbol.COLUMN:
        return Col(args[0])

    elif head == Symbol.PIPELINE:
        pipeline_args, *block = args

        for stmt in block:
            # Adding dataframe as argument
            stmt.insert(1, pipeline_args[0])
            e[pipeline_args[0]] = eval(stmt, e)

        return e[pipeline_args[0]]

    else:
        proc = eval(head, e)
        vals = [eval(arg, e) for arg in args]

        return proc(*vals)


def run(src, env=None):
    return eval(parse(src), e=env)
