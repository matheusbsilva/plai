from lark import Lark
from lark import InlineTransformer
from lark.indenter import Indenter

from .symbol import Symbol

grammar = r"""
?start : _NL* stmt+

?stmt : expr ("as" var)* _NL* -> alias_expr
      | assignment _NL*
      | pipeline _NL*

assignment : NAME "=" stmt

arguments : argvalue("," argvalue)*

?argvalue : expr("=" expr)?

pipeline : "pipeline" "(" arguments+ ")" ":" _NL _INDENT stmt+ _DEDENT

?expr : expr _sum_op term -> binop
      | term

?term : term _mult_op atom_expr -> binop
      | atom_expr

sugar_column : "." var
             | "." string

?atom_expr : atom_expr "(" arguments? ")" -> function_call
           | atom_expr "." NAME -> attr_call
           | sugar_column
           | atom

?atom : NUMBER -> number
      | string
      | var
      | "(" expr ")"

var : NAME

string : ESCAPED_STRING

!_sum_op :  "+" | "-"
!_mult_op : "*" | "/"

%import common.NUMBER -> NUMBER
%import common.CNAME -> NAME
%import common.WS_INLINE
%declare _INDENT _DEDENT
%ignore WS_INLINE

_NL: /(\r?\n[\t ]*)+/
_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\)(\\\\)*?/

ESCAPED_STRING : ("\"" | "'") _STRING_ESC_INNER ("\"" | "'")
"""


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

    plai_parser = Lark(grammar, parser='lalr', transformer=PlaiTransformer(), postlex=TreeIndenter())
    return plai_parser.parse(src)


class PlaiTransformer(InlineTransformer):

    def start(self, *args):
        return [Symbol.BEGIN, *args]

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

    def var(self, token):
        return Symbol(token)

    def sugar_column(self, name):
        return [Symbol.COLUMN, str(name)]

    def pipeline(self, *args):
        pipeline_args, *block = args
        return [Symbol.PIPELINE, pipeline_args, *block]
