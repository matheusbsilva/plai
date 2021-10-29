import tokenize

grammar = r"""
?start : (_NL | stmt)*
       | single_stmt _NL*

?stmt : expr _NL
      | alias_expr _NL
      | assignment _NL
      | type_stmt _NL
      | pipeline

?single_stmt : (expr | alias_expr | assignment | type_stmt)

assignment : NAME "=" expr

type_stmt : "type" NAME "=" expr

arguments : argvalue("," argvalue)*

?argvalue : expr("=" expr)?

pipeline : "pipeline" "(" pipeline_args ")" ":" suite
         | "pipeline" "(" pipeline_args ")" "->" (var | string) ":" suite -> pipeline_output_stmt

pipeline_main_arg : expr[":" var]
pipeline_args : pipeline_main_arg["," arguments]

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


?atom : "(" expr ")"
      | "[" [expr ("," expr)*] "]" -> list_expr
      | "{{" key_content "}}"
      | NUMBER -> number
      | string
      | var
      | "True" -> const_true
      | "False" -> const_false
      | "None" -> const_none

?key_content : _key_value_list? -> dict_expr
             | [expr ("," expr)*] -> slice_df_expr

_key_value_list : key_value("," key_value)*[","]
key_value : expr ":" expr

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
