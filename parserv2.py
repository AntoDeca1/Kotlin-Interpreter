import ply.yacc as yacc
from lexer import tokens

start = "program"

precedence = (
    ('right', 'EQUAL'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('nonassoc', 'LOGICAL_EQUAL', 'NOT_EQUAL'),
    ('nonassoc', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'LOGICAL_NOT', 'UMINUS')
)


def p_program(p):
    'program : statement_list'
    p[0] = p[1]


def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : variable_declaration
                 | function_declaration'''
    p[0] = p[1]


def p_variable_declaration(p):
    '''variable_declaration : VAL ID COLONS type EQUAL expression
                            | VAR ID COLONS type EQUAL expression
                            | VAL ID EQUAL expression
                            | VAR ID EQUAL expression'''
    if len(p) == 6:
        p[0] = p[6]
    else:
        p[0] = p[4]


def p_type(p):
    ''' type : INT
             | STRING
             | BOOLEAN'''
    p[0] = p[1]


def p_expression(p):
    '''expression : aritmetic_expression
                  | boolean_expression
                  | string_expression'''
    p[0] = p[1]


def p_aritmetic_expression(p):
    '''aritmetic_expression : INTEGER_LITERAL
                            | aritmetic_expression PLUS aritmetic_expression
                            | aritmetic_expression MINUS aritmetic_expression
                            | aritmetic_expression TIMES aritmetic_expression
                            | aritmetic_expression DIVIDE aritmetic_expression
                            | LPAREN aritmetic_expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    else:
        p[0] = p[2]


def p_string_expression(p):
    '''string_expression : STRING_LITERAL
                         | string_expression PLUS string_expression
                         | LPAREN string_expression RPAREN '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + p[3]
    else:
        p[0] = p[2]


def p_boolean_expression(p):
    '''boolean_expression : boolean
                         | boolean_expression LOGICAL_AND boolean_expression
                         | boolean_expression LOGICAL_OR boolean_expression
                         | LOGICAL_NOT boolean_expression
                         | aritmetic_expression GREATER_THAN aritmetic_expression
                         | aritmetic_expression LESS_THAN aritmetic_expression
                         | aritmetic_expression LOGICAL_EQUAL aritmetic_expression
                         | aritmetic_expression NOT_EQUAL aritmetic_expression
                         | aritmetic_expression GREATER_THAN_EQUAL aritmetic_expression
                         | aritmetic_expression LESS_THAN_EQUAL aritmetic_expression
                         | LPAREN boolean_expression RPAREN '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "&&":
        p[0] = p[1] and p[3]
    elif p[2] == "||":
        p[0] = p[1] or p[3]
    elif p[1] == "!":
        p[0] = not (p[2])
    elif p[2] == ">":
        p[0] = p[1] > p[3]
    elif p[2] == "<":
        p[0] = p[1] < p[3]
    elif p[2] == "==":
        p[0] = p[1] == p[3]
    elif p[2] == "!=":
        p[0] = p[1] != p[3]
    elif p[2] == ">=":
        p[0] = p[1] >= p[3]
    elif p[2] == "<=":
        p[0] = p[1] <= p[3]
    else:
        p[0] = p[2]


def p_boolean(p):
    '''boolean : TRUE
               | FALSE'''
    if p[1] == 'true':
        p[0] = True
    else:
        p[0] = False


def p_sync(p):
    '''sync : NEWLINE'''
    pass


# NEW(Starting to introduce the function definition)
# TODO: function_declaration to be checked
def p_function_declaration(p):
    '''function_declaration : FUN ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('fun', p[4])


def p_parameter_list(p):
    '''parameter_list : parameter
                     | parameter_list COMMA parameter '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_parameter(p):
    '''parameter : ID COLONS type'''
    p[0] = p[1]


# PANIC MODE
def p_error(p):
    print("Errore Sintattico Attenzione")
    if not p:
        print("End of File!")
        return

    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()  # Get the next token
        if not tok or tok.type == 'NEWLINE':
            break
    parser.restart()


# Build the parser
parser = yacc.yacc()
