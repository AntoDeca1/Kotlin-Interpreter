from parser import initialize_parser
from lexer import initialize_lexer
from visit import Visitor
import sys
import os
from symbol_table import *

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

while True:
    test_number = input("Please input the test script you would like to try [1-2-3-4-5] (Press Enter to exit): ")

    if not test_number:
        break

    test_script_path = os.path.join(base_dir, f'test_scripts/test_{test_number}.kt')

    if not os.path.isfile(test_script_path):
        print(f"File '{test_script_path}' not found.")
        continue

    with open(test_script_path, 'r') as file:
        input_sentence = file.read()

    print("You selected the following script\n")
    print("------------Script-to-be-interpreted---------------------")
    print(input_sentence)

    # Create a new lexer and parser instance for each iteration
    new_lexer = initialize_lexer()
    new_parser = initialize_parser()

    new_lexer.input(input_sentence)
    parsed_result = new_parser.parse(lexer=new_lexer)

    s_t = SymbolTable()
    f_t = FunctionTable()
    ast_flag = input("Do you want to see the resulting AST? [y|n] :")

    if ast_flag == "y":
        print("-----------AST-Construction----------")
        print(parsed_result)
    print("-----------Interpreting----------")
    visitor = Visitor(s_t, f_t)
    visitor.visit(parsed_result)

input("Press Enter to exit...")
