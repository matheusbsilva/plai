import tokenize
import ast

from lark import Lark
from lark import InlineTransformer
from lark.indenter import Indenter

from .symbol import Symbol

grammar = r"""
?start : (_NL | stmt)*
       | single_stmt _NL*

?stmt : expr _NL
      | alias_expr _NL
      | assignment _NL
      | pipeline

?single_stmt : (expr | alias_expr | assignment)

assignment : NAME "=" expr

arguments : argvalue("," argvalue)*

?argvalue : expr("=" expr)?

pipeline : "pipeline" "(" arguments+ ")" ":" suite
         | "pipeline" "(" arguments+ ")" "->" (var | string) ":" suite -> pipeline_output_stmt

suite : _simple_stmt | _NL _INDENT stmt+ _DEDENT

_simple_stmt : single_stmt(";" single_stmt)*

alias_expr : expr ("as" var)

?expr: or_expr

?or_expr : and_expr ("or" or_expr)*

?and_expr : not_expr ("and" and_expr)*

?not_expr : "not" not_expr -> not_op
          | comparison

?comparison : arith_expr _comp_op expr -> bin_op
            | arith_expr

?arith_expr : arith_expr _sum_op term -> bin_op
            | term

?term : term _mult_op atom_expr -> bin_op
      | atom_expr

sugar_column : "." NAME
             | "." string

?atom_expr : atom_expr "(" arguments? ")" -> function_call
           | atom_expr "." NAME -> attr_call
           | sugar_column
           | atom

?atom : NUMBER -> number
      | string
      | var
      | "(" expr ")"
      | "[" [expr ("," expr)*] "]" -> list_expr
      | "{{" [expr ("," expr)*] "}}" -> slice_df_expr
      | "True" -> const_true
      | "False" -> const_false
      | "None" -> const_none

var : NAME

string : STRING

!_sum_op :  "+" | "-"
!_mult_op : "*" | "/" | "//"
!_comp_op : "<" | ">" | "==" | ">=" | "<=" | "!="

NUMBER : /{number}/
STRING : /{string}/
NAME : /{name}/

%import common.WS_INLINE

%declare _INDENT _DEDENT
%ignore WS_INLINE

_NL: /(\r?\n[\t ]*)+/
""".format(number=tokenize.Number, string=tokenize.String, name=tokenize.Name)


class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


def parse(src, return_tree=False):

    if return_tree is True:
        parser = Lark(grammar, parser='lalr')
        return parser.parse(src)

    plai_parser = Lark(grammar,
                       parser='lalr',
                       transformer=PlaiTransformer(),
                       postlex=TreeIndenter())
    return plai_parser.parse(src)


class PlaiTransformer(InlineTransformer):

    def start(self, *sargs):
        return [Symbol.BEGIN, *sargs]

    def number(self, token):
        return ast.literal_eval(token)

    def string(self, token):
        return ast.literal_eval(token)

    def suite(self, *sargs):
        return [*sargs]

    def or_expr(self, right, left):
        return [Symbol('or'), right, left]

    def and_expr(self, right, left):
        return [Symbol('and'), right, left]

    def not_op(self, value):
        return [Symbol('not'), value]

    def bin_op(self, left, op, right):
        return [Symbol(op), left, right]

    def arguments(self, *args):
        return [*args]

    def argvalue(self, *args):
        return [*args]

    def function_call(self, name, args=[]):
        return [name, *args]

    def attr_call(self, obj, attr):
        return [Symbol.ATTR, obj, Symbol(attr)]

    def alias_expr(self, *expr):
        return [Symbol.ALIAS, *expr]

    def assignment(self, name, *stmt):
        return [Symbol.ASSIGNMENT, Symbol(name), *stmt]

    def const_true(self):
        return True

    def const_false(self):
        return False

    def const_none(self):
        return None

    def slice_df_expr(self, *args):
        return [Symbol.SLICE_DF, *args]

    def list_expr(self, *args):
        return [Symbol.LIST, *args]

    def var(self, token):
        return Symbol(token)

    def sugar_column(self, name):
        return [Symbol.COLUMN, str(name)]

    def pipeline(self, *args):
        pipeline_args, *block = args
        return [Symbol.PIPELINE, pipeline_args, *block]

    def pipeline_output_stmt(self, *args):
        pipeline_args, target, *block = args
        pipeline = [Symbol.PIPELINE, pipeline_args, *block]
        return [Symbol.OUTPUT, target, pipeline]
