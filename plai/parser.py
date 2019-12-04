from lark import Lark
from lark import InlineTransformer

from .symbol import Symbol

grammar = r"""
?start : stmt+

?stmt : expr
      | assignment
      | pipeline

assignment : NAME "=" stmt

arguments : expr("," expr)*

pipeline : "pipeline" "(" arguments+ ")" ":" stmt+

?expr : expr _sum_op term -> binop
      | term

?term : term _mult_op atom_expr -> binop
      | atom_expr

?atom_expr : atom_expr "(" arguments? ")" -> function_call
           | atom_expr "." NAME -> attr_call
           | "." atom -> sugar_column
           | atom

?atom : NUMBER -> number
      | STRING -> string
      | NAME -> var
      | "(" expr ")"

!_sum_op :  "+" | "-"
!_mult_op : "*" | "/"

%import common.NUMBER -> NUMBER
%import common.ESCAPED_STRING -> STRING
%import common.CNAME -> NAME

%ignore /\s/
"""


def parse(src, return_tree=False):

    if return_tree is True:
        parser = Lark(grammar, parser='lalr')
        return parser.parse(src)

    plai_parser = Lark(grammar, parser='lalr', transformer=PlaiTransformer())
    return plai_parser.parse(src)


class PlaiTransformer(InlineTransformer):

    def number(self, token):
        return float(token)

    def string(self, token):
        return token[1:-1].replace('\\"', '"')\
                .replace('\\n', '\n')\
                .replace('\\t', '\t')

    def binop(self, left, op, right):
        return [Symbol(op), left, right]

    def arguments(self, *args):
        return [*args]

    def function_call(self, name, *args):
        return [name, *args]

    def attr_call(self, obj, attr):
        return [Symbol.ATTR, obj, Symbol(attr)]

    def assignment(self, name, *stmt):
        return [Symbol('='), Symbol(name), *stmt]

    def var(self, token):
        return Symbol(token)

    def sugar_column(self, name):
        if not isinstance(name, Symbol):
            name = Symbol(name)
        return [Symbol.COLUMN, name]

    def pipeline(self, *args):
        pipeline_args, *block = args
        return [Symbol.PIPELINE, pipeline_args, block]

