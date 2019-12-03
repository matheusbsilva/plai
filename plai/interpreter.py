import operator as op

from .parser import parse
from .symbol import Symbol

builtin_func = {
    Symbol('+'): op.add
}


def eval(sexpr):
    if isinstance(sexpr, Symbol):
        return builtin_func[sexpr]
    elif isinstance(sexpr, (int, float, str)):
        return sexpr
    else:
        head, *args = sexpr
        proc = eval(head)
        vals = [eval(arg) for arg in args]

        return proc(*vals)


def run(src):
    return eval(parse(src))
