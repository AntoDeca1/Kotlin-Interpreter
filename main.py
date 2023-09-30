from parserv2 import parser
from lexer import lexer
import pprint

# Step 2: Tokenize the Input Sentence
input_sentence = '''fun prova(x:String,y:String){ val x=4} 
                    fun prova2(x:String,y:String){val x=4}
                    val x=4
                    var y=12
                    var z= 12+4
                   '''
lexer.input(input_sentence)

# Step 4: Call the Parser
parsed_result = parser.parse(lexer=lexer)

# You can now use the parsed_result as needed
pprint.pprint(parsed_result)
