from parserv2 import parser
from lexer import lexer
import pprint
from visit import Visitor
from symbol_table import *

# Step 2: Tokenize the Input Sentence
input_sentence = '''var z ="Stringa" 
var y=z+6
print(y)
fun prova(x:String){
return x}
print("prova")'''

# Questo dovrebbe essere un errore perchè non ho specificato l'output,allora perchè va bene
lexer.input(input_sentence)

# Step 4: Call the Parser
parsed_result = parser.parse(lexer=lexer)
s_t = SymbolTable()
f_t = FunctionTable()
# You can now use the parsed_result as needed
print("-----------AST-Construction----------")
print(parsed_result)
print("--------------Interpreting-------------")
visitor = Visitor(s_t, f_t)
visitor.visit(parsed_result)
