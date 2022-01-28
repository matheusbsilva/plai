import ast

from lark import InlineTransformer

from plai.symbol import Symbol


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

    def mix_args(self, *sargs):
        return [*sargs]

    def posargs(self, *args):
        return [*args, []]

    def kwargs(self, *args):
        return [*args]

    def argpair(self, name, *expr):
        return [Symbol(name), *expr]

    def function_call(self, name, args=[]):
        return [Symbol.FUNCTION, name, *args]

    def attr_call(self, obj, attr):
        return [Symbol.ATTR, obj, Symbol(attr)]

    def alias_expr(self, *expr):
        return [Symbol.ALIAS, *expr]

    def assignment(self, name, *stmt):
        return [Symbol.ASSIGNMENT, Symbol(name), *stmt]

    def type_stmt(self, name, *stmt):
        return [Symbol.TYPE, Symbol(name), *stmt]

    def typed_stmt(self, name, *stmt):
        return [Symbol.TYPED, Symbol(name), *stmt]

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

    def key_value(self, key, value):
        return [key, value]

    def dict_expr(self, *sargs):
        return [Symbol.DICT, *sargs]

    def var(self, token):
        return Symbol(token)

    def sugar_column(self, name):
        return [Symbol.COLUMN, str(name)]

    def dataframe_attr_call(self, name):
        return [Symbol.DF_ATTR_CALL, Symbol(name)]

    def pipeline_args(self, main_arg):
        return [main_arg]

    def pipeline(self, *args):
        pipeline_args, *block = args
        return [Symbol.PIPELINE, pipeline_args, *block]

    def pipeline_output_stmt(self, *args):
        pipeline_args, target, *block = args
        pipeline = [Symbol.PIPELINE, pipeline_args, *block]
        return [Symbol.OUTPUT, target, pipeline]
