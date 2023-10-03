from symbol_table import SymbolTable
from utilities import *


class Visitor:

    def __init__(self, s_t):
        self.s_t = s_t

    def visit(self, node):
        if node.node_type == "ProgramNode":
            return self.visit(node.children[0])
        elif node.node_type == "StatementList":
            for children in node.children:
                self.visit(children)
            return
        elif node.node_type == "VariableDeclarationNode":
            if len(node.children) == 3:
                id = self.visit(node.children[0])
                type = self.visit(node.children[1])
                expression = self.visit(node.children[2])
                self.s_t.register_variable(id, type, expression)
            else:
                id = self.visit(node.children[0])
                expression = self.visit(node.children[1])
                type = get_type(expression)
                self.s_t.register_variable(id, type, expression)
                print(self.s_t.symbol_tables)
        elif node.node_type == "WhileStatementNode":
            self.s_t.enter_scope()
            while self.visit(node.children[0]):
                self.visit(node.children[1])
            self.s_t.exit_scope()
            return
        elif node.node_type == "AssignmentNode":
            # TODO:Controllo dei tipi
            id = self.visit(node.children[0])
            value = self.visit(node.children[1])
            type = get_type(value)
            self.s_t.modify_variable(id, value, type)
            return
        elif node.node_type == "TermNode":
            return node.leaf
        elif node.node_type == "EmptyNode":
            return
        elif node.node_type == "ExpressionNode":
            return self.visit(node.children[0])
        elif node.node_type == "BinaryExpressionNode":
            return self.binary_expression(node)
        elif node.node_type == "UnaryExpressionNode":
            # TODO:Controllo su un tipo
            operator = node.children[0]
            return not (operator)
        elif node.node_type == "LiteralNode":
            return node.leaf

    def binary_expression(self, node):
        # TODO:Controllo degli errori di tipo
        print("Entro")
        if node.children[0].node_type == "TermNode":
            id = self.visit(node.children[0])
            first_operator = self.s_t.find_variable(id)[1]
            # TODO:Qua sta anche il type nella symbol table
        else:
            first_operator = self.visit(node.children[0])
        if node.children[1].node_type == "TermNode":
            id = self.visit(node.children[1])
            second_operator = self.s_t.find_variable(id)[1]
        else:
            second_operator = self.visit(node.children[1])

        if node.leaf == "+":
            return first_operator + second_operator
        elif node.leaf == "-":
            return first_operator - second_operator
        elif node.leaf == "*":
            return first_operator * second_operator
        elif node.leaf == "/":
            return first_operator / second_operator
        elif node.leaf == ">=":
            return first_operator >= second_operator
        elif node.leaf == "<=":
            return first_operator <= second_operator
        elif node.leaf == "<":
            return first_operator < second_operator
        elif node.leaf == ">":
            return first_operator > second_operator
        elif node.leaf == "==":
            return first_operator == second_operator
        elif node.leaf == "&&":
            return first_operator and second_operator
        elif node.leaf == "||":
            return first_operator or second_operator
        elif node.leaf == "!=":
            return first_operator != second_operator
# TODO:Non posso nella stessa symbol table avere due variabili con lo stesso nome dichiarate
# TODO:Controllare che ci sia sempre un main
