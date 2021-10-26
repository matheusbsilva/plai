from .parser import parse
from .symbol import Symbol
from .modules import Col
from .environment import env


def eval(sexpr, e=None, **kwargs):
    if e is None:
        e = env()

    if isinstance(sexpr, Symbol):
        try:
            value = e[sexpr]
        except KeyError:
            raise NameError('name %s is undefined' % sexpr)
        return value

    elif isinstance(sexpr, (int, float, str, type(None))):
        return sexpr

    head, *sargs = sexpr

    if head == Symbol.ASSIGNMENT:
        var, exp = sargs
        e[var] = eval(exp, e, **kwargs)

    elif head == Symbol.LIST:
        return [eval(arg, e, **kwargs) for arg in sargs]

    elif head == Symbol.COLUMN:
        if 'dataframe' not in kwargs:
            raise NameError('Dataframe not specified for the operation')

        return Col(sargs[0], kwargs['dataframe'])

    elif head == Symbol.ATTR:
        var, call = sargs
        return getattr(e[var], str(call))

    elif head == Symbol.ALIAS:
        expr, name = sargs
        result = eval(expr, **kwargs)
        dataframe = kwargs['dataframe']

        if(isinstance(result, Col)):
            result = result()

        return dataframe.assign(**{str(name): result})

    elif head == Symbol.PIPELINE:
        pipeline_args, *block = sargs
        dataframe = eval(*pipeline_args, e, **kwargs)

        for stmt in block:
            dataframe = eval(stmt, e, **{'dataframe': dataframe})

        return dataframe

    else:
        proc = eval(head, e, **kwargs)
        vals = [eval(sarg, e, **kwargs) for sarg in sargs]

        return proc(*vals, **kwargs)


def run(src, env=None, **kwargs):
    return eval(parse(src), e=env, **kwargs)
