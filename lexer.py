import ply.lex as lex

# List of token names
non_reserved = [
    'ID',
    'EMPTY',
    'PLUS',
    'MINUS',
    'WHITE',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'NOT_EQUAL',
    'NEWLINE',
    'LESS_THAN',
    'GREATER_THAN',
    'LESS_THAN_EQUAL',
    'GREATER_THAN_EQUAL',
    'LOGICAL_AND',
    'LOGICAL_OR',
    'LOGICAL_EQUAL',
    'LOGICAL_NOT',
    'RPAREN',
    'LPAREN',
    'L_BRACE',
    'R_BRACE',
    'COLONS',  #:
    'STRING_LITERAL',
    'INTEGER_LITERAL',
]

# Define reserved words
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'fun': 'FUNCTION',
    'while': 'WHILE',
    'Int': 'INT',
    'Boolean': 'BOOLEAN',
    'String': 'STRING',
    'println': 'PRINT',
    'true': 'TRUE',
    'false': 'FALSE',
    'var': 'VAR',
    'val': 'VAL',
    'readLine': 'READLINE'
}

tokens = non_reserved + list(reserved.values())
# TODO: Gestire la questione dello scope
t_ignore = ' \t'

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_EQUAL = r'\='
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_COLONS = r'\:'
t_GREATER_THAN_EQUAL = r'\>='
t_LESS_THAN_EQUAL = r'\<='
t_NOT_EQUAL = r'\!='
t_LESS_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_LOGICAL_EQUAL = r'\=\='
t_LOGICAL_OR = r'\|\|'
t_LOGICAL_AND = r'\&&'
t_LOGICAL_NOT = r'\!'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_white(t):
    'r\s+'
    pass


def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    # Match Everything that starts with a letter or underscore and is followed by 0 or more letters,underscores,numbers
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


lexer = lex.lex()
# input_sentence = '''var x =  "Kevin" + "Rodolfo" '''
#
# lexer.input(input_sentence)
#
# # Step 3: Iterate over the tokens
# while True:
#     token = lexer.token()
#     if not token:
#         break  # No more tokens
#     print(token)
