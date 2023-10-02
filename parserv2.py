import ply.yacc as yacc
from lexer import tokens
from Node import *
from utilities import *

symbol_tables = [{}]

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


def p_empty(p):
    'empty :'
    pass


def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_program(p):
    'program : statement_list'
    p[0] = Node("ProgramNode", children=[p[1]])


def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = Node("StatementList", children=[p[1]])
    else:
        p[1].add_child(p[2])
        p[0] = p[1]


def p_statement(p):
    '''statement : variable_declaration
                 | function_declaration
                 | function_calling
                 | if_statement
                 | while_statement
                 | output_statement'''
    # Evitiamo lo statementNode
    p[0] = p[1]


def p_sync(p):
    '''sync : NEWLINE'''
    pass


# NEW(Starting to introduce the function definition)
# TODO: function_declaration to be checked
def p_function_declaration(p):
    '''function_declaration : FUN ID LPAREN parameter_list RPAREN COLONS type LBRACE statement_list RBRACE
                            | FUN ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE'''


def p_function_calling(p):
    '''function_calling : ID LPAREN parameter_list RPAREN
                        | VAL ID COLONS type EQUAL ID LPAREN parameter_list RPAREN
                        | VAR ID COLONS type EQUAL ID LPAREN parameter_list RPAREN
                        | VAL ID EQUAL ID LPAREN parameter_list RPAREN
                        | VAR ID EQUAL ID LPAREN parameter_list RPAREN'''


def p_parameter_list(p):
    '''parameter_list : parameter
                     | parameter_list COMMA parameter'''


def p_parameter(p):
    '''parameter : ID COLONS type
                 | ID'''


# NEW(Starting to introduce the if else statement)
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE RBRACE
                    | IF LPAREN expression RPAREN LBRACE RBRACE ELSE LBRACE RBRACE
                    | IF LPAREN expression RPAREN LBRACE RBRACE'''

    # Introdotta la possibilità di avere anche if e else vuoti


# NEW(Starting to introduce the while statement)
def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
                       | WHILE LPAREN expression RPAREN LBRACE RBRACE'''


# NEW(Starting to introduce the input statement)
# def p_input_statement(p):
#     '''input_statement : READLINE LPAREN expression'''
#     pass


# NEW(Starting to introduce the output statement)
def p_output_statement(p):
    '''output_statement : PRINT LPAREN expression RPAREN'''
    p[0] = ("print", p[3])


def p_variable_declaration(p):
    '''variable_declaration : VAL ID COLONS type EQUAL expression
                            | VAR ID COLONS type EQUAL expression
                            | VAL ID EQUAL expression
                            | VAR ID EQUAL expression  '''
    # TODO:Da controllare come idea, per evitare di creare un altra classe salvare in leaf var/val
    # TODO:Qui ID non ha un nodo perchè non diventa mai term
    id_Node = Node("TermNode", leaf=p[2])
    if len(p) == 7:
        p[0] = Node("VariableDeclarationNode", children=[id_Node, p[4], p[6]], leaf=p[1])
    else:
        # TODO:Non posso inferire il tipo da qui,vedere se serve o se possiamo farlo in fase di discesa
        p[0] = Node("VariableDeclarationNode", children=[id_Node, p[4]], leaf=p[1])


def p_type(p):
    ''' type : INT
             | STRING
             | BOOLEAN'''
    p[0] = Node("TypeNode", leaf=p[1])


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
    if len(p) == 2:
        p[0] = p[1]  # Se passo da term ad expression non creo un expressionNode ma lo creo solo alla fine
    elif len(p) == 4 and p[1] == "(":
        p[0] = p[2]
    elif len(p) == 3:
        operator = Node("UnaryExpressionNode", leaf=p[1], children=[p[2]])
        p[0] = Node("ExpressionNode", children=operator, leaf="=")
    else:
        operator = Node("BinaryExpressionNode", leaf=p[2], children=[p[1], p[3]])
        p[0] = Node("ExpressionNode", children=[operator], leaf="=")


def p_term(p):
    '''term : Literal
            | ID'''
    if isinstance(p[1], Node):
        p[0] = p[1]
    else:
        p[0] = Node("TermNode", leaf=p[1])


def p_literal(p):
    '''Literal : INTEGER_LITERAL
                | TRUE
                | FALSE
                | STRING_LITERAL'''
    p[0] = Node("LiteralNode", leaf=p[1])


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
