from parser import parser
from lexer import lexer
from visit import Visitor
from symbol_table import *

with open('test_scripts/test_4.kt', 'r') as file:
    input_sentence = file.read()

lexer.input(input_sentence)
parsed_result = parser.parse(lexer=lexer)

s_t = SymbolTable()
f_t = FunctionTable()
print("-----------AST-Construction----------")
print(parsed_result)
print("-----------Interpreting----------")
visitor = Visitor(s_t, f_t)
visitor.visit(parsed_result)
