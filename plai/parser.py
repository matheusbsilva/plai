from lark import Lark

grammar = r"""
start : expr

?expr : func
      | atom
      | pipe

func : SYMBOL "(" (atom ("," atom)*)? ")"

pipe : func "|>" expr

?atom : NUMBER
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
