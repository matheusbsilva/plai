from lark import Lark
from lark import InlineTransformer

from plai.symbol import Symbol
from plai.parser.ast import AST

grammar = r"""
?start : stmt+

?stmt : expr
      | assignment
      | pipeline

assignment : NAME "=" stmt

arguments : expr("," expr)*

pipeline : "pipeline" "(" arguments+ ")" ":" "{" stmt+ "}"

?expr : expr _sum_op term -> binop
      | term

?term : term _mult_op atom_expr -> binop
      | atom_expr

sugar_column : "." name
             | "." string

?atom_expr : atom_expr "(" arguments? ")" -> function_call
           | atom_expr ATTR_CALL name -> attr_call
           | sugar_column
           | atom

?atom : NUMBER -> number
      | string
      | name
      | "(" expr ")"

name: NAME

string : STRING

ATTR_CALL : "."

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

    def start(self, *args):
        return [Symbol.BEGIN, *args]

    def number(self, token):
        return AST(token)

    def string(self, token):
        return AST(token)

    def binop(self, left, op, right):
        return [Symbol(op), left, right]

    def arguments(self, *args):
        return [*args]

    def function_call(self, name, args=[]):
        return [name, *args]

    def attr_call(self, obj, attr_symbol, attr):
        node = AST(attr_symbol)
        node.add_child(obj)
        node.add_child(attr)

        return node

    def assignment(self, name, *stmt):
        return [Symbol.ASSIGNMENT, Symbol(name), *stmt]

    def name(self, token):
        return AST(token)

    def sugar_column(self, name):
        return [Symbol.COLUMN, str(name)]

    def pipeline(self, *args):
        pipeline_args, *block = args
        return [Symbol.PIPELINE, pipeline_args, *block]
