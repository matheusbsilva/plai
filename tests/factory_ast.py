from plai.parser.ast import AST
from lark import Token


def number_node(value):
    return AST(Token('NUMBER', value))


def string_node(value):
    return AST(Token('STRING', value))


def name_node(value):
    return AST(Token('NAME', value))


def attr_call_node(value_obj, value_attr):
    node = AST(Token('ATTR_CALL', '.'))
    node.add_child(name_node(value_obj))
    node.add_child(name_node(value_attr))

    return node


def assign_node():
    return AST(Token('ASSIGN', '='))


def generic_node(token_type, token_value):
    return AST(Token(token_type, token_value))


def op_node(op):
    ops_symbol = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'STAR',
        '/': 'SLASH'
    }

    return AST(Token(ops_symbol[op], op))


def binop_node(op, left, right):
    node = op_node(op)
    node.add_child(number_node(left))
    node.add_child(number_node(right))

    return node
