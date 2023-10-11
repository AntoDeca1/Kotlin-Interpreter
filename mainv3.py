from parserv3 import parser
from lexer import lexer
from visit import Visitor
from symbol_table import *

# input_sentence = '''
#                     fun main() {
#                         val x :Int="Prova"
#                     }
#                     '''
with open('test_scripts/test_5.kt', 'r') as file:
    input_sentence = file.read()

# Questo dovrebbe essere un errore perchè non ho specificato l'output,allora perchè va bene
lexer.input(input_sentence)
# Step 4: Call the Parser
parsed_result = parser.parse(lexer=lexer)
s_t = SymbolTable()
f_t = FunctionTable()
print("-----------AST-Construction----------")
print(parsed_result)
visitor = Visitor(s_t, f_t)
visitor.visit(parsed_result)
