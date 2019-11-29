from lark import Lark
from lark import InlineTransformer

from .symbol import Symbol

grammar = r"""
?start : stmt

?stmt : expr
      | function_call

function_call : NAME "(" arguments? ")"

arguments : expr("," expr)*

?term : term _mult_op atom -> binop
      | atom

?expr : expr _sum_op term -> binop
      | term

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


def parse(src):
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

    def function_call(self, name, args):
        return [Symbol(name), args]
