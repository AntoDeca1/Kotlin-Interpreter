from parserv2 import parser
from lexer import lexer
import pprint

# Step 2: Tokenize the Input Sentence
input_sentence = ''' print(10+x)
                   '''
lexer.input(input_sentence)

# Step 4: Call the Parser
parsed_result = parser.parse(lexer=lexer)

# You can now use the parsed_result as needed
pprint.pprint(parsed_result)
