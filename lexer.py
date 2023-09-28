import ply.lex as lex

# List of token names
non_reserved = [
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'NOT_EQUAL',
    'LESS_THAN',
    'GRATER_THAN',
    'LESS_THAN_EQUAL',
    'GREATER_THAN_EQUAL',
    'LOGICAL_AND',
    'LOGICAL_OR',
    'LOGICAL_NOT',
    'RPAREN',
    'LPAREN',
    'L_BRACE',
    'R_BRACE',
    'COLONS',  #:
    'STRING_LITERAL',
    'INTEGER_LITERAL'
]

# Define reserved words
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'fun': 'FUNCTION',
    'for': 'FOR',
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
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_COLONS = r'\:'
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


def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'\"[^\"]*\"'
    return t


def t_ID(t):
    # Match Everything that starts with a letter or underscore and is followed by 0 or more letters,underscores,numbers
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# Test it out
data = '''
val name : String ="Nate"
'''
lexer = lex.lex()
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
