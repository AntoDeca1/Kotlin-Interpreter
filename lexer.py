import ply.lex as lex

non_reserved = [
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'COMMA',
    'EQUAL',
    'NOT_EQUAL',
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
    'LBRACE',
    'RBRACE',
    'COLONS',
    'SEMICOLON',
    'STRING_LITERAL',
    'INTEGER_LITERAL',
    'RANGE'
]

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'fun': 'FUN',
    'while': 'WHILE',
    'for': 'FOR',
    'Int': 'INT',
    'Boolean': 'BOOLEAN',
    'String': 'STRING',
    'print': 'PRINT',
    'true': 'TRUE',
    'false': 'FALSE',
    'var': 'VAR',
    'val': 'VAL',
    'readLine': 'READLINE',
    'return': 'RETURN',
    'step': 'STEP',
    'in': 'IN'
}

tokens = non_reserved + list(reserved.values())
t_ignore = ' \t'

t_PLUS = r'\+'
t_EQUAL = r'\='
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLONS = r'\:'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_GREATER_THAN_EQUAL = r'\>='
t_LESS_THAN_EQUAL = r'\<='
t_NOT_EQUAL = r'\!='
t_LESS_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_LOGICAL_EQUAL = r'\=\='
t_LOGICAL_OR = r'\|\|'
t_LOGICAL_AND = r'\&&'
t_LOGICAL_NOT = r'\!'
t_RANGE = r'\..'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL \
                (t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def initialize_lexer():
    return lex.lex()
