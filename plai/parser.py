from lark import Lark

grammar = r"""
start : expr

expr : function_defition
      | function_call
      | atom
      | pipeline

function_defition : "def" SYMBOL args ":" block
function_call : SYMBOL args

args : "(" (arg("," arg)*)? ")"

arg : atom (":" atom)?

pipeline : "pipeline" args ":" block

block : expr+

atom : NUMBER
      | STRING
      | SYMBOL

SYMBOL : /[-+!@$\/\\*%^&~<>|=\w]+/
%import common.SIGNED_NUMBER -> NUMBER
%import common.ESCAPED_STRING -> STRING

%ignore /\s/
"""

def parse(src):
    plai_parser = Lark(grammar)

    return plai_parser.parse(src)
