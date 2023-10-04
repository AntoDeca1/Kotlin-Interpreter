from symbol_table import *
from utilities import *


class Visitor:

    def __init__(self, s_t, f_t):
        self.s_t = s_t
        self.f_t = f_t

    def visit(self, node):
        if node.node_type == "ProgramNode":
            return self.visit(node.children[0])
        elif node.node_type == "StatementList":
            for children in node.children:
                result = self.visit(children)
                if result is not None:
                    return result
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
        elif node.node_type == "If-else-StatementNode":
            condition = self.visit(node.children[0])
            if condition:
                self.s_t.enter_scope()
                statement_list = self.visit(node.children[1])
                self.s_t.exit_scope()
                return statement_list
            else:
                self.s_t.enter_scope()
                statement_list = self.visit(node.children[2])
                self.s_t.exit_scope()
                return statement_list
        elif node.node_type == "IfStatementNode":
            condition = self.visit(node.children[0])
            if condition:
                self.s_t.enter_scope()
                statement_list = self.visit(node.children[1])
                self.s_t.exit_scope()
                return statement_list
        elif node.node_type == "AssignmentNode":
            # TODO:Controllo dei tipi
            id = self.visit(node.children[0])
            value = self.visit(node.children[1])
            type = get_type(value)
            variable_type = self.s_t.find_variable(id)[0]
            if variable_type == type:
                self.s_t.modify_variable(id, value, type)
            else:
                raise Exception("Type Mismatch")
            return
        elif node.node_type == "FunctionDeclarationNode":
            if len(node.children) == 4:
                function_name = self.visit(node.children[0])
                parameter_list = self.visit(node.children[1])
                output_type = self.visit(node.children[2])
                stataments_list = node.children[3]
                self.f_t.register_function(function_name, parameter_list, stataments_list, output_type)
            else:
                function_name = self.visit(node.children[0])
                parameter_list = self.visit(node.children[1])
                stataments_list = node.children[2]
                self.f_t.register_function(function_name, parameter_list, stataments_list)
            return
        elif node.node_type == "FunctionCallingNode":
            function_name = self.visit(node.children[0])
            input_parameters = self.visit(node.children[1])
            input_types = [get_type(parameter) for parameter in input_parameters]
            parameter_list, statament_list, output_type = self.f_t.find_variable(function_name)
            correct_types = [parameter[1] for parameter in parameter_list]
            if input_types == correct_types:
                # TODO:Gestire il return e l'output type
                result = self.visit(statament_list)
                result_type = get_type(result)
                if result_type != output_type:
                    raise Exception("Type Mismatch")
                else:
                    return result
            else:
                raise Exception(f"Parameters Mismatch")

        elif node.node_type == "ReturnNode":
            if node.children[0].node_type == "TermNode":
                result = self.check_if_st(node.children[0])
                return result
            else:
                return self.visit(node.children[0])
        elif node.node_type == "ParameterDeclarationNode":
            parameter_name = self.visit(node.children[0])
            parameter_type = self.visit(node.children[1])
            return (parameter_name, parameter_type)
        elif node.node_type == "ParameterListCalling":
            parameters = []
            for children in node.children:
                if children.node_type == "TermNode":
                    temp_parameter = self.check_if_st(children)
                else:
                    temp_parameter = self.visit(children)
                parameters.append(temp_parameter)
            return parameters
        elif node.node_type == "ParameterListDeclaration":
            parameters = []
            for children in node.children:
                temp_parameter = self.visit(children)
                parameters.append(temp_parameter)
            return parameters
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
        elif node.node_type == "TypeNode":
            return node.leaf
        elif node.node_type == "LiteralNode":
            return node.leaf

    def binary_expression(self, node):
        # TODO:Controllo degli errori di tipo
        print("Entro")
        first_operator = self.check_if_st(node.children[0])
        second_operator = self.check_if_st(node.children[1])
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

    def check_if_st(self, node):
        if node.node_type == "TermNode":
            id = self.visit(node)
            return self.s_t.find_variable(id)[1]
            # TODO:Qua sta anche il type nella symbol table
        else:
            return self.visit(node)

# TODO:Non posso nella stessa symbol table avere due variabili con lo stesso nome dichiarate
# TODO:Controllare che ci sia sempre un main
# TODO: Fare un symbol tables per funzioni
# TODO: Entrare anche nello scope delle funzioni
# TODO :Controllo valore in output della funzione
# TODO : Return Keyword
# TODO: Return con function_calling gestire che l'output della funzione sia effettivamente quello che ritorniamo
# TODO :Rendere metodi privati
