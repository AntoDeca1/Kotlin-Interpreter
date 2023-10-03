from parserv2 import parser
from lexer import lexer
import pprint
from visit import Visitor
from symbol_table import SymbolTable

# Step 2: Tokenize the Input Sentence
input_sentence = '''val x= 10
                    while(x>5){x=2}'''
lexer.input(input_sentence)

# Step 4: Call the Parser
parsed_result = parser.parse(lexer=lexer)
s_t = SymbolTable()

# You can now use the parsed_result as needed
print(parsed_result)
visitor = Visitor(s_t)
visitor.visit(parsed_result)
