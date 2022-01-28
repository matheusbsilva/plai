from lark import Lark
from lark.indenter import Indenter

from .grammar import grammar
from .transformer import PlaiTransformer


class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


def parse(src, return_tree=False):

    if return_tree is True:
        parser = Lark(grammar, parser='lalr', postlex=TreeIndenter())
        return parser.parse(src)

    plai_parser = Lark(grammar,
                       parser='lalr',
                       transformer=PlaiTransformer(),
                       postlex=TreeIndenter())
    return plai_parser.parse(src)
