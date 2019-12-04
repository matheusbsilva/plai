from .symbol import Symbol


def env(variables=None):
    if variables:
        if any(not isinstance(key, Symbol) for key in variables):
            raise TypeError('variables must be instance of Symbol')
        return variables
    else:
        return {}
