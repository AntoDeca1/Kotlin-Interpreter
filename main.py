from parserv2 import parser
from lexer import lexer

# Step 2: Tokenize the Input Sentence
input_sentence = '''var x =  "Kevin" + "Rodolfo" '''
lexer.input(input_sentence)

# Step 4: Call the Parser
parsed_result = parser.parse(lexer=lexer)

# You can now use the parsed_result as needed
print(parsed_result)
