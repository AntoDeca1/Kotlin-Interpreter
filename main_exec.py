from parser import parser
from lexer import lexer
from visit import Visitor
import sys
import os
from symbol_table import *

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
test_number = input("Please input the test script you would like to try[1-2-3-4-5] : ")
ast_flag = input("Do you want to see also the resulting AST? [y|n]")
test_script_path = os.path.join(base_dir, f'test_scripts/test_{test_number}.kt')
print(test_script_path)
if not os.path.isfile(test_script_path):
    print(f"File '{test_script_path}' not found.")
    sys.exit(1)

with open(test_script_path, 'r') as file:
    input_sentence = file.read()

print("You selected the following script\n")
print("------------Script-to-be-interpreted---------------------")
print(input_sentence)
lexer.input(input_sentence)
parsed_result = parser.parse(lexer=lexer)

s_t = SymbolTable()
f_t = FunctionTable()
if ast_flag == "y":
    print("-----------AST-Construction----------")
    print(parsed_result)
print("-----------Interpreting----------")
visitor = Visitor(s_t, f_t)
visitor.visit(parsed_result)
input("Press Enter to exit...")
