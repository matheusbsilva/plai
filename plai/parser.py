from lark import Lark
from lark import InlineTransformer

grammar = r"""
?start : expr

?expr : function_defition
      | function_call
      | atom
      | pipeline

function_defition : "def" SYMBOL args ":" block
function_call : SYMBOL args

args : "(" (arg("," arg)*)? ")"

arg : atom (":" atom)?

pipeline : "pipeline" args ":" block

block : expr+

?atom : NUMBER -> number
      | STRING -> string
      | SYMBOL -> symbol

SYMBOL : /[-+!@$\/\\*%^&~<>|=\w]+/

%import common.SIGNED_NUMBER -> NUMBER
%import common.ESCAPED_STRING -> STRING

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
