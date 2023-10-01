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
                 | function_declaration
                 | if_statement
                 | while_statement
                 | output_statement'''
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
    '''expression : term
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LOGICAL_AND expression
                  | expression LOGICAL_OR expression
                  | expression LOGICAL_EQUAL expression
                  | LOGICAL_NOT expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN expression
                  | expression NOT_EQUAL expression
                  | expression GREATER_THAN_EQUAL expression
                  | expression LESS_THAN_EQUAL expression
                  | LPAREN expression RPAREN '''
    print("Ciao")
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
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


def p_term(p):
    '''term : Literal
            | ID'''
    if isinstance(p[1], str) and len(p[1]) == 1:
        p[0] = 5
    else:
        p[0] = p[1]


def p_literal(p):
    '''Literal : INTEGER_LITERAL
               | boolean
               | STRING_LITERAL'''
    p[0] = p[1]


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


# NEW(Starting to introduce the if else statement)
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    p[0] = ("if", p[3])


# NEW(Starting to introduce the while statement)
def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = ("while", p[3])


# NEW(Starting to introduce the input statement)
# def p_input_statement(p):
#     '''input_statement : READLINE LPAREN expression'''
#     pass


# NEW(Starting to introduce the output statement)
def p_output_statement(p):
    '''output_statement : PRINT LPAREN expression RPAREN'''
    p[0] = ("print", p[3])


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
