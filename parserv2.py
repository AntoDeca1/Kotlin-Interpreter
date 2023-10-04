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
                 | output_statement
                 | assignment
                 | return_statement'''
    # Evitiamo lo statementNode
    p[0] = p[1]


def p_sync(p):
    '''sync : NEWLINE'''
    pass


# NEW(Starting to introduce the function definition)
# TODO: function_declaration to be checked
def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = Node("ReturnNode", children=[p[2]])


# return var prova String = prova(x,y)
def p_assignment(p):
    '''assignment : ID EQUAL expression'''
    id_node = Node("TermNode", leaf=p[1])
    p[0] = Node("AssignmentNode", children=[id_node, p[3]])


def p_function_declaration(p):
    '''function_declaration : FUN ID LPAREN parameter_list_declaration RPAREN COLONS type LBRACE statement_list RBRACE
                            | FUN ID LPAREN parameter_list_declaration RPAREN LBRACE statement_list RBRACE
                            | FUN ID LPAREN parameter_list_declaration RPAREN LBRACE RBRACE'''
    id_node = Node("TermNode", leaf=p[2])
    if len(p) == 10:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, p[4], p[7], p[9]])
    elif len(p) == 9:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, p[4], p[7]])
    else:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, p[4], Node("EmptyNode", leaf=" ")])


def p_function_calling(p):
    '''function_calling : ID LPAREN parameter_list_calling RPAREN
                        | VAL ID COLONS type EQUAL ID LPAREN parameter_list_calling RPAREN
                        | VAR ID COLONS type EQUAL ID LPAREN parameter_list_calling RPAREN
                        | VAL ID EQUAL ID LPAREN parameter_list_calling RPAREN
                        | VAR ID EQUAL ID LPAREN parameter_list_calling RPAREN
                        | ID EQUAL ID LPAREN parameter_list_calling RPAREN'''
    if len(p) == 5:
        id_node = Node("TermNode", leaf=p[1])
        p[0] = Node("FunctionCallingNode", children=[id_node, p[3]])
    elif len(p) == 10:
        var_id_node = Node("TermNode", leaf=p[2])
        fun_id_node = Node("TermNode", leaf=p[6])
        function_calling_node = Node("FunctionCallingNode", children=[fun_id_node, p[8]])
        p[0] = Node("VariableDeclarationNode", children=[var_id_node, p[4], p[7], function_calling_node], leaf=p[1])
    elif len(p) == 7:
        var_id_node = Node("TermNode", leaf=p[1])
        fun_id_node = Node("TermNode", leaf=p[3])
        function_calling_node = Node("FunctionCallingNode", children=[fun_id_node, p[5]])
        p[0] = Node("AssignmentNode", children=[var_id_node, function_calling_node])
    else:
        var_id_node = Node("TermNode", leaf=p[2])
        fun_id_node = Node("TermNode", leaf=p[4])
        function_calling_node = Node("FunctionCallingNode", children=[fun_id_node, p[6]])
        p[0] = Node("VariableDeclarationNode", children=[var_id_node, function_calling_node], leaf=p[1])


def p_parameter_list_calling(p):
    '''parameter_list_calling : parameter_calling
                              | parameter_list_calling COMMA parameter_calling'''
    if len(p) == 2:
        p[0] = Node("ParameterListCalling", children=[p[1]])
    else:
        p[1].add_child(p[3])
        p[0] = p[1]


def p_parameter_list_declaration(p):
    '''parameter_list_declaration : parameter_declaration
                                  | parameter_list_declaration COMMA parameter_declaration'''
    if len(p) == 2:
        p[0] = Node("ParameterListDeclaration", children=[p[1]])
    else:
        p[1].add_child(p[3])
        p[0] = p[1]


# def fun(x:String,y:Prova)
# fun(x,y)

def p_parameter_calling(p):
    '''parameter_calling : term'''
    # Nel caso in cui siano una lista di id,semplicemente ritornare il termNode
    p[0] = p[1]


def p_parameter_declaration(p):
    '''parameter_declaration : ID COLONS type'''
    # Nel caso in cui siano una lista di id,semplicemente ritornare il termNode
    id_node = Node("TermNode", leaf=p[1])
    p[0] = Node("ParameterDeclarationNode", children=[id_node, p[3]])


# NEW(Starting to introduce the if else statement)
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE RBRACE ELSE LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE RBRACE
                    | IF LPAREN expression RPAREN LBRACE RBRACE ELSE LBRACE RBRACE
                    | IF LPAREN expression RPAREN LBRACE RBRACE'''

    # Introdotta la possibilità di avere anche if e else vuoti
    # TODO:Vedere se è meglio non mettere nulla quando non ci sono statement oppure creare un EmptyNode??(Per adesso non metto nulla)
    if len(p) == 8:
        p[0] = Node("IfStatementNode", children=[p[3], p[6]])
    elif len(p) == 12:
        p[0] = Node("If-else-StatementNode", children=[p[3], p[6], p[10]])
    elif len(p) == 11 and isinstance(p[9], Node):
        p[0] = Node("If-else-StatementNode", children=[p[3], Node("EmptyNode", leaf=" "), p[9]])
    elif len(p) == 11 and isinstance(p[6], Node):
        p[0] = Node("If-else-StatementNode", children=[p[3], p[6], Node("EmptyNode", leaf=" ")])
    elif len(p) == 10 and isinstance(p[6], Node):
        p[0] = Node("If-else-StatementNode", children=[p[3], Node("EmptyNode", leaf=" "), Node("EmptyNode", leaf=" ")])
    else:
        p[0] = Node("IfStatementNode", children=[p[3], Node("EmptyNode", leaf=" ")])


# NEW(Starting to introduce the while statement)


def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
                       | WHILE LPAREN expression RPAREN LBRACE RBRACE'''
    if len(p) == 8:
        p[0] = Node("WhileStatementNode", children=[p[3], p[6]])
    else:
        p[0] = Node("WhileStatementNode", children=[p[3], Node("EmptyNode", leaf=" ")])


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

    # 3+2
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
