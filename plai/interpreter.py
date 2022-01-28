import os

import pandas as pd

from .parser import parse
from .symbol import Symbol
from .modules import Col
from .environment import env
from .validation import validate_schema


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

        return e[var]

    elif head == Symbol.LIST:
        return [eval(arg, e, **kwargs) for arg in sargs]

    elif head == Symbol.DICT:
        return {eval(key, e, **kwargs): eval(value, e, **kwargs) for key, value in sargs}

    elif head == Symbol.TYPE:
        name, exp = sargs
        type_definition = eval(exp, e, **kwargs)

        if not isinstance(type_definition, dict):
            raise ValueError('type must be a dict')

        e[name] = type_definition

    elif head == Symbol.SLICE_DF:
        cols = [eval(arg, e, **kwargs) for arg in sargs]

        # TODO: return specific element or error
        if any(not isinstance(col, Col) for col in cols):
            raise ValueError('Values must be columns')

        return pd.concat([col() for col in cols], axis=1)

    elif head == Symbol.COLUMN:
        if 'dataframe' not in kwargs:
            raise NameError('Dataframe not specified for the operation')

        return Col(sargs[0], kwargs['dataframe'])

    elif head == Symbol.ATTR:
        var, call = sargs

        var = eval(var, e, **kwargs)
        return getattr(var, str(call))

    elif head == Symbol.ALIAS:
        expr, name = sargs
        result = eval(expr, **kwargs)
        dataframe = kwargs['dataframe']

        if(isinstance(result, Col)):
            result = result()

        return dataframe.assign(**{str(name): result})

    elif head == Symbol.OUTPUT:
        target, pipeline = sargs
        pipeline_result = eval(pipeline, e, **kwargs)

        if(isinstance(target, Symbol)):
            e[target] = pipeline_result
        elif(isinstance(target, str)):
            _, ext = os.path.splitext(target)

            if(ext != '.csv'):
                # TODO: support multiple files type
                raise ValueError('File type not supported')

            pipeline_result.to_csv(target, index=False)

        return pipeline_result

    elif head == Symbol.TYPED:
        type_def, args = sargs
        dataframe = eval(args, e, **kwargs)

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError('Type can only be checked on DataFrame')

        schema = eval(type_def, e, **kwargs)
        validation = validate_schema(dataframe, schema)

        if 'errors' in validation:
            msg = '\n'.join(validation['errors'])
            raise ValueError(msg)

        return dataframe

    elif head == Symbol.PIPELINE:
        pipeline_args, block = sargs

        dataframe = eval(*pipeline_args, e, **kwargs)

        for stmt in block:
            dataframe = eval(stmt, e, dataframe=dataframe)

        return dataframe

    elif head == Symbol.DF_ATTR_CALL:
        dataframe = kwargs['dataframe']

        return getattr(dataframe, str(*sargs))

    elif head == Symbol.FUNCTION:
        func_call, *func_args = sargs
        proc = eval(func_call, e, **kwargs)
        posargs = ()
        nkwargs = {}

        if func_args:
            *rposargs, rkwargs = func_args
            posargs = []

            for arg in rposargs:
                value = eval(arg, e, **kwargs)

                if(isinstance(value, Col)):
                    value = value()

                posargs.append(value)

            for rkwarg in rkwargs:
                key, key_raw_value = rkwarg
                key_value = eval(key_raw_value, e, **kwargs)

                if(isinstance(key_value, Col)):
                    key_value = key_value()

                nkwargs[str(key)] = key_value

        return proc(*posargs, **nkwargs)
    else:
        proc = eval(head, e, **kwargs)
        vals = [eval(sarg, e, **kwargs) for sarg in sargs]

        return proc(*vals)


def run(src, env=None, **kwargs):
    return eval(parse(src), e=env, **kwargs)
