import ply.yacc as yacc
from lexer import *
from Node import *
from exceptions import *

# Start symbol of the grammar
start = "program"

# Precedence and associativity
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


# Rule to use empty string inside the productions
def p_empty(p):
    'empty :'
    pass


# Rule to give to this expression the precedence specified above
def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    operator = Node("UnaryExpressionNode", leaf=p[1], children=[p[2]], lineno=p[2].lineno)
    p[0] = Node("ExpressionNode", children=[operator], leaf="=", lineno=p[2].lineno)


def p_program(p):
    'program : declarations'
    p[0] = Node("ProgramNode", children=[p[1]])


def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement '''
    if len(p) == 2:
        p[0] = Node("StatementList", children=[p[1]])
    else:
        p[1].add_child(p[2])
        p[0] = p[1]


def p_declarations(p):
    '''declarations : declaration
                    | declarations declaration '''
    if len(p) == 2:
        p[0] = Node("StatementList", children=[p[1]])
    else:
        p[1].add_child(p[2])
        p[0] = p[1]


def p_declaration(p):
    '''declaration : variable_declaration semis
                   | function_declaration semis '''
    p[0] = p[1]


def p_statement(p):
    '''statement : declaration
                 | function_calling semis
                 | if_statement semis
                 | while_statement semis
                 | for_statement semis
                 | assignment semis
                 | return_statement semis
                 | print_statement semis'''
    p[0] = p[1]


def p_block(p):
    '''block : LBRACE RBRACE
             | LBRACE statement_list RBRACE'''
    if len(p) == 3:
        p[0] = Node("EmptyNode", leaf="")
    else:
        p[0] = p[2]


def p_return_statement(p):
    '''return_statement : RETURN expression'''
    lineno = p.slice[1].lineno
    p[0] = Node("ReturnNode", children=[p[2]], lineno=lineno)


def p_assignment(p):
    '''assignment : ID EQUAL expression'''
    lineno = p.slice[1].lineno
    id_node = Node("TermNode", leaf=p[1], lineno=lineno)
    p[0] = Node("AssignmentNode", children=[id_node, p[3]])


def p_function_declaration(p):
    '''function_declaration : FUN ID LPAREN parameter_list_declaration RPAREN COLONS type block
                            | FUN ID LPAREN parameter_list_declaration RPAREN block
                            | FUN ID LPAREN RPAREN COLONS type block
                            | FUN ID LPAREN RPAREN block'''
    lineno = p.slice[2].lineno
    id_node = Node("TermNode", leaf=p[2], lineno=lineno)
    if len(p) == 9:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, p[4], p[7], p[8]])
    elif len(p) == 7:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, p[4], p[6]])
    elif len(p) == 8:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, Node("EmptyNode", leaf=" "), p[6], p[7]])
    else:
        p[0] = Node("FunctionDeclarationNode", children=[id_node, Node("EmptyNode", leaf=" "), p[5]])


def p_function_calling(p):
    '''function_calling : ID LPAREN parameter_list_calling RPAREN
                        | ID LPAREN RPAREN'''
    lineno = p.slice[1].lineno
    id_node = Node("TermNode", leaf=p[1], lineno=lineno)
    if len(p) == 5:
        p[0] = Node("FunctionCallingNode", children=[id_node, p[3]])
    else:
        p[0] = Node("FunctionCallingNode", children=[id_node, Node("EmptyNode", leaf="")])


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
        p[0] = p[1]
    elif len(p) == 4 and p[1] == "(":
        p[0] = p[2]
    elif len(p) == 3:
        operator = Node("UnaryExpressionNode", leaf=p[1], children=[p[2]], lineno=p[2].lineno)
        p[0] = Node("ExpressionNode", children=[operator], leaf="=", lineno=p[2].lineno)
    else:
        operator = Node("BinaryExpressionNode", leaf=p[2], children=[p[1], p[3]], lineno=p[1].lineno)
        p[0] = Node("ExpressionNode", children=[operator], leaf="=", lineno=p[1].lineno)


def p_parameter_calling(p):
    '''parameter_calling : term'''
    p[0] = p[1]


def p_parameter_declaration(p):
    '''parameter_declaration : ID COLONS type'''
    id_node = Node("TermNode", leaf=p[1])
    p[0] = Node("ParameterDeclarationNode", children=[id_node, p[3]])


def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block'''
    if len(p) == 6:
        p[0] = Node("IfStatementNode", children=[p[3], p[5]])

    else:
        p[0] = Node("If-else-StatementNode", children=[p[3], p[5], p[7]])


def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block'''
    p[0] = Node("WhileStatementNode", children=[p[3], p[5]])


def p_for_statement(p):
    '''for_statement : FOR LPAREN range_operator RPAREN block '''
    p[0] = Node("ForStatement", children=[p[3], p[5]])


def p_range_operator(p):
    '''range_operator : ID IN term RANGE term
                      | ID IN term RANGE term STEP term'''
    id_Node = Node("TermNode", leaf=p[1])
    if len(p) == 6:
        p[0] = Node("RangeOperator", children=[id_Node, p[3], p[5]])
    else:
        p[0] = Node("RangeOperator", children=[id_Node, p[3], p[5], p[7]])


def p_variable_declaration(p):
    '''variable_declaration : VAL ID COLONS type EQUAL expression
                            | VAR ID COLONS type EQUAL expression
                            | VAL ID EQUAL expression
                            | VAR ID EQUAL expression  '''
    id_Node = Node("TermNode", leaf=p[2], lineno=p.slice[2].lineno)
    if len(p) == 7:
        p[0] = Node("VariableDeclarationNode", children=[id_Node, p[4], p[6]], leaf=p[1])
    else:
        p[0] = Node("VariableDeclarationNode", children=[id_Node, p[4]], leaf=p[1])


def p_type(p):
    ''' type : INT
             | STRING
             | BOOLEAN'''
    lineno = p.slice[1].lineno
    p[0] = Node("TypeNode", leaf=p[1], lineno=lineno)


def p_print(p):
    '''print_statement : PRINT LPAREN expression RPAREN'''
    p[0] = Node("PrintStatementNode", children=[p[3]])


def p_term(p):
    '''term : Literal
            | ID
            | function_calling
            | readline'''
    if isinstance(p[1], Node):
        p[0] = p[1]
    else:
        lineno = p.slice[1].lineno
        p[0] = Node("TermNode", leaf=p[1], lineno=lineno)


def p_literal(p):
    '''Literal : INTEGER_LITERAL
                | TRUE
                | FALSE
                | STRING_LITERAL'''
    lineno = p.slice[1].lineno
    p[0] = Node("LiteralNode", leaf=p[1], lineno=lineno)


def p_semis(p):
    '''semis : SEMICOLON
             | empty'''


def p_readline(p):
    '''readline : READLINE LPAREN RPAREN'''
    p[0] = Node("ReadlineNode")


# Syntax error handling
def p_error(p):
    line = p.lineno
    token = p.value
    error_message = f"Error at line {line}: Unexpected token '{token}'"
    print(error_message)
    raise ParserError(error_message)


parser = yacc.yacc()


def initialize_parser():
    return yacc.yacc()
